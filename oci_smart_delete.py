#!/usr/bin/env python3
"""
OCI Smart Delete - Optimized compartment cleanup tool

This tool combines the best of OCI-SuperDelete and ociextirpater:
1. Uses OCI Search service to discover what resources actually exist
2. Only processes resource types that are found (massive speed improvement)
3. Parallel processing across regions
4. Handles dependencies and retries

Usage:
    python3 oci_smart_delete.py -c <compartment_ocid> [-force] [-cp <profile>]
"""

import oci
import sys
import argparse
import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import importlib

# Import comprehensive resource type mappings
try:
    from oci_resource_types import RESOURCE_TYPE_MAP
except ImportError:
    print("Error: oci_resource_types.py not found!")
    print("Run: python3 generate_comprehensive_mappings.py")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class OCISmartDelete:
    """Smart OCI resource deletion using Search-first approach"""

    # Use imported comprehensive resource type mappings
    # This is populated from oci_resource_types.py which contains 124+ resource types
    RESOURCE_TYPE_MAP = RESOURCE_TYPE_MAP

    # Legacy small map (kept for reference, overridden by import above)
    _LEGACY_MAP = {
        'Instance': {
            'client': 'compute.ComputeClient',
            'method': 'terminate_instance',
            'composite': 'compute.ComputeClientCompositeOperations',
            'composite_method': 'terminate_instance_and_wait_for_state',
            'wait_states': ['TERMINATED'],
            'id_field': 'id'
        },
        'VolumeAttachment': {
            'client': 'compute.ComputeClient',
            'method': 'detach_volume',
            'id_field': 'id'
        },
        'Volume': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_volume',
            'composite': 'core.BlockstorageClientCompositeOperations',
            'composite_method': 'delete_volume_and_wait_for_state',
            'wait_states': ['TERMINATED'],
            'id_field': 'id'
        },
        'BootVolume': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_boot_volume',
            'id_field': 'id'
        },
        'Bucket': {
            'client': 'object_storage.ObjectStorageClient',
            'method': 'delete_bucket',
            'id_field': 'name',
            'special': 'bucket'  # Needs namespace
        },
        'Vcn': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_vcn',
            'id_field': 'id',
            'dependencies': ['Subnet', 'InternetGateway', 'NatGateway', 'ServiceGateway', 'RouteTable', 'SecurityList', 'Drg']
        },
        'Subnet': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_subnet',
            'id_field': 'id'
        },
        'InternetGateway': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_internet_gateway',
            'id_field': 'id'
        },
        'NatGateway': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_nat_gateway',
            'id_field': 'id'
        },
        'ServiceGateway': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_service_gateway',
            'id_field': 'id'
        },
        'RouteTable': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_route_table',
            'id_field': 'id'
        },
        'SecurityList': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_security_list',
            'id_field': 'id'
        },
        'Drg': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_drg',
            'id_field': 'id'
        },
        'DrgAttachment': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_drg_attachment',
            'id_field': 'id'
        },
        'LoadBalancer': {
            'client': 'load_balancer.LoadBalancerClient',
            'method': 'delete_load_balancer',
            'id_field': 'id'
        },
        'DbSystem': {
            'client': 'database.DatabaseClient',
            'method': 'terminate_db_system',
            'id_field': 'id'
        },
        'AutonomousDatabase': {
            'client': 'database.DatabaseClient',
            'method': 'delete_autonomous_database',
            'id_field': 'id'
        },
        'Function': {
            'client': 'functions.FunctionsManagementClient',
            'method': 'delete_function',
            'id_field': 'id'
        },
        'Application': {
            'client': 'functions.FunctionsManagementClient',
            'method': 'delete_application',
            'id_field': 'id',
            'dependencies': ['Function']
        },
        'Cluster': {
            'client': 'container_engine.ContainerEngineClient',
            'method': 'delete_cluster',
            'id_field': 'id'
        },
        'NodePool': {
            'client': 'container_engine.ContainerEngineClient',
            'method': 'delete_node_pool',
            'id_field': 'id'
        },
        'ContainerInstance': {
            'client': 'container_instances.ContainerInstanceClient',
            'method': 'delete_container_instance',
            'id_field': 'id'
        },
        'App': {  # GenAI Agent resources
            'client': 'generative_ai_agent.GenerativeAiAgentClient',
            'method': 'delete_agent',
            'id_field': 'id'
        },
        'FssReplicationTarget': {
            'client': 'file_storage.FileStorageClient',
            'method': 'delete_replication_target',
            'id_field': 'id'
        },
        'Group': {  # IAM Group
            'client': 'identity.IdentityClient',
            'method': 'delete_group',
            'id_field': 'id'
        },
    }

    def __init__(self, config, signer, compartment_id, regions=None, force=False, max_retries=3, delete_compartment=False):
        self.config = config
        self.signer = signer
        self.compartment_id = compartment_id
        self.force = force
        self.max_retries = max_retries
        self.delete_compartment = delete_compartment
        self.clients = {}
        self.regions = regions or self._get_subscribed_regions()

        # Track deletion stats
        self.deleted_count = defaultdict(int)
        self.failed_count = defaultdict(int)

        # Progress tracking for real-time feedback
        self.progress = {
            'total_resources': 0,
            'processed': 0,
            'deleted': 0,
            'failed': 0,
            'current_type': '',
            'current_resource': '',
            'status': 'idle',  # idle, discovering, deleting, cleanup, complete
            'resources_status': {},  # {resource_id: {name, type, status, error}}
            'phase': '',
            'processed_ids': set()  # Track which resources have been counted in 'processed'
        }

    def _get_subscribed_regions(self):
        """Get all subscribed regions"""
        identity = oci.identity.IdentityClient(self.config, signer=self.signer)
        regions = identity.list_region_subscriptions(self.config['tenancy']).data
        return [r.region_name for r in regions if r.status == 'READY']

    def _get_client(self, client_path, region):
        """Get or create a client for a specific region"""
        key = f"{client_path}:{region}"
        if key not in self.clients:
            config = self.config.copy()
            config['region'] = region

            # Parse client path (e.g., 'core.ComputeClient')
            parts = client_path.split('.')
            # Import the module dynamically
            module = importlib.import_module(f'oci.{parts[0]}')
            client_class = getattr(module, parts[1])

            self.clients[key] = client_class(config, signer=self.signer)

        return self.clients[key]

    def discover_resources(self):
        """
        Use OCI Search service to discover all resources in compartment
        Returns: dict mapping resource types to lists of resources
        """
        logger.info(f"Discovering resources in compartment {self.compartment_id}...")

        search_client = oci.resource_search.ResourceSearchClient(
            self.config, signer=self.signer
        )

        # Query for all resources in compartment that aren't already deleted
        query = f"""query all resources where
                    compartmentId = '{self.compartment_id}' &&
                    lifecycleState != 'TERMINATED' &&
                    lifecycleState != 'DELETED' &&
                    lifecycleState != 'DELETING' &&
                    lifecycleState != 'TERMINATING'"""

        resources_by_type = defaultdict(list)

        try:
            # Handle pagination
            page = None
            while True:
                search_details = oci.resource_search.models.StructuredSearchDetails(
                    query=query,
                    type='Structured',
                    matching_context_type='NONE'
                )

                if page:
                    response = search_client.search_resources(
                        search_details,
                        page=page,
                        limit=1000
                    )
                else:
                    response = search_client.search_resources(
                        search_details,
                        limit=1000
                    )

                for item in response.data.items:
                    resources_by_type[item.resource_type].append(item)

                if not response.has_next_page:
                    break
                page = response.next_page

        except Exception as e:
            logger.error(f"Error discovering resources: {e}")
            return {}

        # Log what we found
        total = sum(len(resources) for resources in resources_by_type.values())
        logger.info(f"Found {total} resources across {len(resources_by_type)} resource types")

        for resource_type, resources in sorted(resources_by_type.items()):
            logger.info(f"  {resource_type}: {len(resources)}")

        return resources_by_type

    def _delete_resource(self, resource, resource_type_config, region, retry_count=0):
        """Delete a single resource"""
        resource_id = resource.identifier
        resource_name = getattr(resource, 'display_name', resource.identifier)

        try:
            # Update progress - mark as deleting
            if retry_count == 0:  # Only mark as deleting on first attempt
                self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleting')
                self.progress['current_resource'] = resource_name

            logger.info(f"Deleting {resource.resource_type}: {resource_name} (ID: {resource_id})")

            # Get the appropriate client
            client = self._get_client(resource_type_config['client'], region)

            # Special handling for buckets (need namespace)
            if resource_type_config.get('special') == 'bucket':
                namespace = client.get_namespace().data
                getattr(client, resource_type_config['method'])(
                    namespace_name=namespace,
                    bucket_name=resource_id
                )
            # Special handling for log analytics entities (need namespace)
            elif resource_type_config.get('special') == 'log_analytics_entity':
                # Log Analytics namespace is the same as Object Storage namespace
                # Get it from Object Storage client
                object_storage_client = self._get_client('object_storage.ObjectStorageClient', region)
                namespace = object_storage_client.get_namespace().data
                getattr(client, resource_type_config['method'])(
                    namespace_name=namespace,
                    log_analytics_entity_id=resource_id
                )
            else:
                # Standard deletion
                delete_method = getattr(client, resource_type_config['method'])

                # Try composite operation if available (waits for completion)
                if 'composite' in resource_type_config:
                    composite_client_path = resource_type_config['composite']
                    parts = composite_client_path.split('.')
                    # Import the module dynamically
                    module = importlib.import_module(f'oci.{parts[0]}')
                    composite_class = getattr(module, parts[1])
                    composite_client = composite_class(client)

                    composite_method = getattr(composite_client, resource_type_config['composite_method'])
                    composite_method(
                        resource_id,
                        wait_for_states=resource_type_config['wait_states']
                    )
                else:
                    delete_method(resource_id)

            # Success!
            self.deleted_count[resource.resource_type] += 1
            self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleted')
            logger.info(f"✓ Deleted {resource.resource_type}: {resource_name}")
            return True

        except oci.exceptions.ServiceError as e:
            # Handle specific errors
            if e.status == 404:
                logger.debug(f"Resource already deleted: {resource_id}")
                self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleted')
                return True
            elif e.status == 409:  # Conflict - usually dependency issue
                if retry_count < self.max_retries:
                    logger.warning(f"Dependency conflict deleting {resource_id}, will retry later")
                    # Don't update status yet - we'll retry
                    return False
                else:
                    logger.error(f"Failed to delete {resource_id} after {self.max_retries} retries: {e.message}")
                    self.failed_count[resource.resource_type] += 1
                    self._update_resource_status(resource_id, resource_name, resource.resource_type, 'failed', e.message)
                    return False
            else:
                logger.error(f"Error deleting {resource_id}: {e.message}")
                self.failed_count[resource.resource_type] += 1
                self._update_resource_status(resource_id, resource_name, resource.resource_type, 'failed', e.message)
                return False
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Unexpected error deleting {resource_id}: {error_msg}")
            self.failed_count[resource.resource_type] += 1
            self._update_resource_status(resource_id, resource_name, resource.resource_type, 'failed', error_msg)
            return False

    def _get_deletion_order(self, resource_types):
        """
        Determine deletion order based on dependencies
        Returns list of resource types in order they should be deleted
        """
        # Build dependency graph
        has_dependencies = []
        no_dependencies = []

        for rtype in resource_types:
            config = self.RESOURCE_TYPE_MAP.get(rtype, {})
            if 'dependencies' in config:
                has_dependencies.append(rtype)
            else:
                no_dependencies.append(rtype)

        # Delete things without dependencies first, then things with dependencies
        return no_dependencies + has_dependencies

    def delete_resources_by_type(self, resource_type, resources):
        """Delete all resources of a specific type"""
        config = self.RESOURCE_TYPE_MAP.get(resource_type)

        if not config:
            logger.warning(f"No deletion config for {resource_type}, skipping")
            return

        logger.info(f"\n{'='*80}")
        logger.info(f"Deleting {len(resources)} {resource_type} resources")
        logger.info(f"{'='*80}")

        # Group by region for parallel processing
        by_region = defaultdict(list)
        for resource in resources:
            # Extract region from resource identifier or availability domain
            region = resource.region if hasattr(resource, 'region') else self.config['region']
            by_region[region].append(resource)

        # Track failed resources for retry
        failed_resources = []

        # Process each region
        for retry in range(self.max_retries + 1):
            if retry > 0:
                if not failed_resources:
                    break
                logger.info(f"\nRetry attempt {retry}/{self.max_retries} for {len(failed_resources)} failed resources")
                time.sleep(5 * retry)  # Exponential backoff

            resources_to_try = failed_resources if retry > 0 else resources
            failed_resources = []

            # Use thread pool for parallel deletion within each region
            with ThreadPoolExecutor(max_workers=min(10, len(resources_to_try))) as executor:
                futures = {}
                for resource in resources_to_try:
                    region = resource.region if hasattr(resource, 'region') else self.config['region']
                    future = executor.submit(
                        self._delete_resource,
                        resource,
                        config,
                        region,
                        retry
                    )
                    futures[future] = resource

                # Collect results
                for future in as_completed(futures):
                    resource = futures[future]
                    try:
                        success = future.result()
                        if not success:
                            failed_resources.append(resource)
                    except Exception as e:
                        logger.error(f"Exception in deletion task: {e}")
                        failed_resources.append(resource)

    def _delete_compartment_itself(self):
        """Delete the compartment itself after all resources are cleaned up"""
        logger.info(f"\n{'='*80}")
        logger.info("Deleting Compartment")
        logger.info(f"{'='*80}")

        try:
            # Get compartment details
            identity_client = oci.identity.IdentityClient(self.config, signer=self.signer)

            try:
                compartment = identity_client.get_compartment(self.compartment_id).data
                logger.info(f"Compartment Name: {compartment.name}")
                logger.info(f"Compartment OCID: {compartment.id}")
                logger.info(f"Current State: {compartment.lifecycle_state}")
            except oci.exceptions.ServiceError as e:
                if e.status == 404:
                    logger.warning("Compartment not found or already deleted")
                    return
                else:
                    raise

            # Check if already deleting
            if compartment.lifecycle_state in ['DELETING', 'DELETED']:
                logger.info(f"Compartment is already in state: {compartment.lifecycle_state}")
                return

            # Confirm deletion if not forced
            if not self.force:
                logger.warning("\n⚠️  WARNING: You are about to DELETE the compartment itself!")
                logger.warning("This action cannot be undone.")
                response = input("\nType 'DELETE' to confirm compartment deletion: ")
                if response != 'DELETE':
                    logger.info("Compartment deletion cancelled")
                    return

            # Delete the compartment
            logger.info("\nDeleting compartment...")
            logger.info("Note: Compartment deletion can take up to 2 hours to complete")

            identity_client.delete_compartment(self.compartment_id)

            logger.info("✓ Compartment deletion initiated successfully")
            logger.info(f"\nCompartment '{compartment.name}' is now being deleted")
            logger.info("You can check the status in the OCI Console under Identity > Compartments")

            # Check if we can get updated status
            try:
                time.sleep(2)
                updated_compartment = identity_client.get_compartment(self.compartment_id).data
                logger.info(f"Current Status: {updated_compartment.lifecycle_state}")
            except:
                pass

        except oci.exceptions.ServiceError as e:
            if e.status == 409:
                logger.error(f"Cannot delete compartment: {e.message}")
                logger.error("The compartment may still have resources or sub-compartments")
            elif e.status == 404:
                logger.warning("Compartment not found - may have been already deleted")
            else:
                logger.error(f"Error deleting compartment: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error deleting compartment: {e}")

    def _update_resource_status(self, resource_id, name, resource_type, status, error=None):
        """Update progress for a specific resource"""
        # Get previous status to handle counter updates properly
        prev_status = self.progress['resources_status'].get(resource_id, {}).get('status')

        # Update the status
        self.progress['resources_status'][resource_id] = {
            'name': name,
            'type': resource_type,
            'status': status,  # 'pending', 'deleting', 'deleted', 'failed'
            'error': error
        }

        # Only count as processed once per resource (when moving from pending to any active status)
        if resource_id not in self.progress['processed_ids'] and status in ['deleting', 'deleted', 'failed']:
            self.progress['processed_ids'].add(resource_id)
            self.progress['processed'] += 1

        # Update deleted/failed counts (only when transitioning to these final states)
        if status == 'deleted' and prev_status != 'deleted':
            self.progress['deleted'] += 1
        elif status == 'failed' and prev_status != 'failed':
            self.progress['failed'] += 1

    def _cleanup_vcn_dependencies(self, resources_by_type):
        """
        Clean up VCN circular dependencies before deletion.
        This clears route table rules that reference gateways.
        """
        self.progress['status'] = 'cleanup'
        self.progress['phase'] = 'Cleaning up VCN dependencies'
        logger.info("\n" + "="*80)
        logger.info("Phase 1: Cleaning up VCN dependencies")
        logger.info("="*80)

        if 'RouteTable' not in resources_by_type:
            return

        try:
            # Get VirtualNetworkClient for the compartment's region
            network_client = self._get_client('core.VirtualNetworkClient', self.config['region'])

            for route_table in resources_by_type['RouteTable']:
                try:
                    rt_id = route_table.identifier
                    rt_name = getattr(route_table, 'display_name', rt_id)

                    # Get current route table
                    rt = network_client.get_route_table(rt_id).data

                    # Check if it has any rules
                    if rt.route_rules and len(rt.route_rules) > 0:
                        logger.info(f"Clearing {len(rt.route_rules)} route rules from: {rt_name}")

                        # Update route table with empty rules
                        network_client.update_route_table(
                            rt_id=rt_id,
                            update_route_table_details=oci.core.models.UpdateRouteTableDetails(
                                route_rules=[]
                            )
                        )
                        logger.info(f"✓ Cleared route rules from: {rt_name}")
                        time.sleep(0.5)  # Brief pause to let changes propagate

                except oci.exceptions.ServiceError as e:
                    if e.status == 404:
                        logger.debug(f"Route table already deleted: {rt_id}")
                    else:
                        logger.warning(f"Could not clear route table {rt_id}: {e.message}")
                except Exception as e:
                    logger.warning(f"Error clearing route table {rt_id}: {e}")

            logger.info("✓ VCN dependency cleanup complete")

        except Exception as e:
            logger.warning(f"Error during VCN cleanup: {e}")
            # Continue anyway - regular deletion may still work

    def delete_all(self):
        """Main deletion workflow"""
        # Initialize progress
        self.progress['status'] = 'discovering'
        self.progress['phase'] = 'Discovering resources'

        # Discover what's actually in the compartment
        resources_by_type = self.discover_resources()

        if not resources_by_type:
            logger.info("No resources found in compartment!")
            self.progress['status'] = 'complete'
            # Delete compartment if requested, even if it's empty
            if self.delete_compartment:
                self._delete_compartment_itself()
            return

        # Initialize progress tracking
        total_resources = sum(len(r) for r in resources_by_type.values())
        self.progress['total_resources'] = total_resources

        # Mark all resources as pending initially
        for rtype, resources in resources_by_type.items():
            for resource in resources:
                resource_id = resource.identifier
                resource_name = getattr(resource, 'display_name', resource_id)
                self._update_resource_status(resource_id, resource_name, rtype, 'pending')

        # Reset counters
        self.progress['processed'] = 0
        self.progress['deleted'] = 0
        self.progress['failed'] = 0

        # Confirm deletion
        if not self.force:
            print(f"\nFound {total_resources} resources to delete:")
            for rtype, resources in sorted(resources_by_type.items()):
                print(f"  - {rtype}: {len(resources)}")

            response = input("\nType 'yes' to confirm deletion: ")
            if response.lower() != 'yes':
                logger.info("Deletion cancelled by user")
                self.progress['status'] = 'cancelled'
                return

        start_time = time.time()

        # Phase 1: Clean up VCN dependencies
        self._cleanup_vcn_dependencies(resources_by_type)

        # Phase 2: Delete resources in dependency order
        self.progress['status'] = 'deleting'
        self.progress['phase'] = 'Deleting resources'
        logger.info("\n" + "="*80)
        logger.info("Phase 2: Deleting resources")
        logger.info("="*80)

        deletion_order = self._get_deletion_order(resources_by_type.keys())

        for resource_type in deletion_order:
            if resource_type in resources_by_type:
                self.progress['current_type'] = resource_type
                self.delete_resources_by_type(resource_type, resources_by_type[resource_type])

        # Mark as complete
        self.progress['status'] = 'complete'
        self.progress['phase'] = 'Deletion complete'

        # Print summary
        elapsed = time.time() - start_time
        logger.info(f"\n{'='*80}")
        logger.info(f"Deletion Summary (completed in {elapsed:.1f} seconds)")
        logger.info(f"{'='*80}")

        total_deleted = sum(self.deleted_count.values())
        total_failed = sum(self.failed_count.values())

        logger.info(f"Successfully deleted: {total_deleted} resources")
        if total_failed > 0:
            logger.info(f"Failed to delete: {total_failed} resources")
            logger.info("\nFailed resource types:")
            for rtype, count in sorted(self.failed_count.items()):
                logger.info(f"  - {rtype}: {count}")

        # Delete compartment if requested and no failures
        if self.delete_compartment:
            if total_failed > 0:
                logger.warning(f"\nSkipping compartment deletion - {total_failed} resources failed to delete")
                logger.warning("Clean up failed resources first, then delete the compartment manually")
            else:
                self._delete_compartment_itself()


def main():
    parser = argparse.ArgumentParser(
        description='OCI Smart Delete - Fast compartment cleanup using Search service'
    )
    parser.add_argument('-c', '--compartment', required=True,
                       help='Compartment OCID to delete')
    parser.add_argument('-cp', '--config-profile', default='DEFAULT',
                       help='Config profile to use (default: DEFAULT)')
    parser.add_argument('-cf', '--config-file', default='~/.oci/config',
                       help='Config file path (default: ~/.oci/config)')
    parser.add_argument('-force', '--force', action='store_true',
                       help='Force deletion without confirmation')
    parser.add_argument('-rg', '--regions',
                       help='Comma-separated list of regions (default: all subscribed)')
    parser.add_argument('-debug', '--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--delete-compartment', action='store_true',
                       help='Delete the compartment itself after cleaning up resources')

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load OCI config
    config = oci.config.from_file(args.config_file, args.config_profile)
    signer = oci.signer.Signer(
        tenancy=config['tenancy'],
        user=config['user'],
        fingerprint=config['fingerprint'],
        private_key_file_location=config['key_file'],
        pass_phrase=config.get('pass_phrase')
    )

    regions = args.regions.split(',') if args.regions else None

    # Create and run deleter
    deleter = OCISmartDelete(
        config=config,
        signer=signer,
        compartment_id=args.compartment,
        regions=regions,
        force=args.force,
        delete_compartment=args.delete_compartment
    )

    deleter.delete_all()


if __name__ == '__main__':
    main()
