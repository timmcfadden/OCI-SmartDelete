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

    # Resource types that should be skipped during deletion because they are:
    # - Auto-deleted when their parent resource is deleted
    # - Cannot be explicitly deleted (managed resources)
    # - Don't have a proper delete API
    SKIP_RESOURCE_TYPES = {
        'PrivateIp',       # Primary IPs are auto-deleted with VNICs/Instances
        'Vnic',            # Auto-deleted when Instance is terminated
        'DnsResolver',     # Auto-managed by VCN, no delete API
        'DnsView',         # Auto-managed by VCN, protected resource
        'CustomerDnsZone', # Auto-managed by VCN, protected resource
        'BootVolumeAttachment',  # Auto-deleted when Instance is terminated
        'VolumeAttachment',      # Auto-deleted when Instance is terminated
        'DrgRouteTable',         # Auto-deleted when DRG is deleted (default tables can't be deleted)
        'DrgRouteDistribution',  # Auto-deleted when DRG is deleted (default distributions can't be deleted)
    }

    # Resource types that cannot be discovered via OCI Resource Search API
    # These need to be listed directly using their respective clients
    NON_SEARCHABLE_RESOURCE_TYPES = {
        'NetworkLoadBalancer': {
            'client': 'network_load_balancer.NetworkLoadBalancerClient',
            'list_method': 'list_network_load_balancers',
            'list_kwargs': lambda compartment_id: {'compartment_id': compartment_id},
            'items_attr': 'items',
            'id_attr': 'id',
            'name_attr': 'display_name',
            'state_attr': 'lifecycle_state',
            'skip_states': ['DELETED', 'DELETING'],
        },
    }

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
                    # Skip resource types that are auto-deleted with their parent
                    if item.resource_type not in self.SKIP_RESOURCE_TYPES:
                        resources_by_type[item.resource_type].append(item)

                if not response.has_next_page:
                    break
                page = response.next_page

        except Exception as e:
            logger.error(f"Error discovering resources: {e}")
            return {}

        # Also discover non-searchable resources (not indexed by OCI Resource Search API)
        self._discover_non_searchable_resources(resources_by_type)

        # Log what we found
        total = sum(len(resources) for resources in resources_by_type.values())
        logger.info(f"Found {total} resources across {len(resources_by_type)} resource types")

        for resource_type, resources in sorted(resources_by_type.items()):
            logger.info(f"  {resource_type}: {len(resources)}")

        return resources_by_type

    def _discover_non_searchable_resources(self, resources_by_type):
        """Discover resources that are not indexed by OCI Resource Search API"""

        # Simple wrapper class to match search result structure
        class NonSearchableResource:
            def __init__(self, identifier, name, res_type):
                self.identifier = identifier
                self.display_name = name
                self.resource_type = res_type

        for resource_type, config in self.NON_SEARCHABLE_RESOURCE_TYPES.items():
            try:
                client = self._get_client(config['client'], self.region)
                list_method = getattr(client, config['list_method'])
                list_kwargs = config['list_kwargs'](self.compartment_id)

                # Handle pagination
                resources = []
                page = None
                while True:
                    if page:
                        list_kwargs['page'] = page
                    response = list_method(**list_kwargs)

                    items = getattr(response.data, config['items_attr'], response.data)
                    if items is None:
                        items = []

                    for item in items:
                        # Check lifecycle state
                        state = getattr(item, config['state_attr'], None)
                        if state and state in config['skip_states']:
                            continue

                        # Create a wrapper object that matches the search result format
                        resource_id = getattr(item, config['id_attr'])
                        display_name = getattr(item, config['name_attr'], resource_id)
                        resources.append(NonSearchableResource(resource_id, display_name, resource_type))

                    if not hasattr(response, 'has_next_page') or not response.has_next_page:
                        break
                    page = response.next_page

                if resources:
                    resources_by_type[resource_type].extend(resources)
                    logger.info(f"  Discovered {len(resources)} non-searchable {resource_type} resources")

            except Exception as e:
                logger.warning(f"Error discovering non-searchable {resource_type} resources: {e}")

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

            # Get the appropriate client (skip for special types that need custom client creation)
            special_type = resource_type_config.get('special')
            if special_type not in ('key',):  # Types that need custom client creation
                client = self._get_client(resource_type_config['client'], region)
            else:
                client = None  # Will be created in special handling

            # Special handling for buckets (need namespace and bucket name, not OCID)
            if special_type == 'bucket':
                namespace = client.get_namespace().data
                # Use display_name for bucket name, not the OCID
                bucket_name = resource_name

                # First, delete all objects in the bucket
                try:
                    # List and delete all objects (including multipart uploads)
                    logger.info(f"Emptying bucket: {bucket_name}")

                    # Delete all objects
                    object_list = client.list_objects(namespace, bucket_name, fields='name').data
                    while object_list.objects:
                        for obj in object_list.objects:
                            client.delete_object(namespace, bucket_name, obj.name)
                        if object_list.next_start_with:
                            object_list = client.list_objects(
                                namespace, bucket_name,
                                start=object_list.next_start_with,
                                fields='name'
                            ).data
                        else:
                            break

                    # Abort any multipart uploads
                    uploads = client.list_multipart_uploads(namespace, bucket_name).data
                    for upload in uploads:
                        client.abort_multipart_upload(namespace, bucket_name, upload.object, upload.upload_id)

                    # Delete all preauthenticated requests
                    pars = client.list_preauthenticated_requests(namespace, bucket_name).data
                    for par in pars:
                        try:
                            client.delete_preauthenticated_request(namespace, bucket_name, par.id)
                        except Exception as par_e:
                            logger.warning(f"Error deleting PAR {par.id}: {par_e}")

                except Exception as e:
                    logger.warning(f"Error emptying bucket {bucket_name}: {e}")

                # Now delete the bucket
                client.delete_bucket(namespace, bucket_name)
            # Special handling for Vault deletion (needs schedule_vault_deletion_details)
            elif special_type == 'vault':
                # Schedule vault deletion for the minimum waiting period (7 days)
                from datetime import datetime, timedelta
                deletion_time = datetime.utcnow() + timedelta(days=7)
                schedule_details = oci.key_management.models.ScheduleVaultDeletionDetails(
                    time_of_deletion=deletion_time
                )
                client.schedule_vault_deletion(resource_id, schedule_details)
                logger.info(f"Vault scheduled for deletion on {deletion_time.isoformat()}")
            # Special handling for Key deletion (needs vault's management endpoint)
            elif special_type == 'key':
                # Keys require the management endpoint from their parent vault
                # Extract vault ID from key ID (format: ocid1.key.oc1.<region>.<vault_id>.<key_id>)
                # We need to look up the vault to get its management endpoint
                try:
                    # Get the key's vault by listing vaults in compartment
                    vault_client = self._get_client('key_management.KmsVaultClient', region)
                    vaults = vault_client.list_vaults(self.compartment_id).data

                    # Find the vault that contains this key by checking if key ID contains vault's crypto endpoint portion
                    key_vault = None
                    for vault in vaults:
                        if vault.lifecycle_state in ['ACTIVE', 'PENDING_DELETION']:
                            # Key ID contains a portion that matches the vault
                            if vault.id.split('.')[-2] in resource_id:
                                key_vault = vault
                                break

                    if not key_vault:
                        # Try to get vault from the key's ID pattern
                        # Key OCID format: ocid1.key.oc1.<region>.<vault_crypto_endpoint_id>.<key_suffix>
                        for vault in vaults:
                            if vault.lifecycle_state in ['ACTIVE', 'PENDING_DELETION']:
                                key_vault = vault
                                break

                    if key_vault and key_vault.management_endpoint:
                        # Create KmsManagementClient with the vault's management endpoint
                        config_copy = self.config.copy()
                        config_copy['region'] = region
                        kms_client = oci.key_management.KmsManagementClient(
                            config_copy,
                            service_endpoint=key_vault.management_endpoint,
                            signer=self.signer
                        )
                        # Schedule key deletion
                        from datetime import datetime, timedelta
                        deletion_time = datetime.utcnow() + timedelta(days=7)
                        schedule_details = oci.key_management.models.ScheduleKeyDeletionDetails(
                            time_of_deletion=deletion_time
                        )
                        kms_client.schedule_key_deletion(resource_id, schedule_details)
                        logger.info(f"Key scheduled for deletion on {deletion_time.isoformat()}")
                    else:
                        logger.warning(f"Could not find active vault for key {resource_id}, skipping")
                        # Mark as success since the vault might already be scheduled for deletion
                        self.deleted_count[resource.resource_type] += 1
                        self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleted')
                        return True
                except Exception as e:
                    logger.warning(f"Error scheduling key deletion: {e}")
                    raise
            # Special handling for log analytics entities (need namespace)
            elif special_type == 'log_analytics_entity':
                # Log Analytics namespace is the same as Object Storage namespace
                # Get it from Object Storage client
                object_storage_client = self._get_client('object_storage.ObjectStorageClient', region)
                namespace = object_storage_client.get_namespace().data
                getattr(client, resource_type_config['method'])(
                    namespace_name=namespace,
                    log_analytics_entity_id=resource_id
                )
            # Special handling for Log resources (need log_group_id and log_id)
            elif special_type == 'log':
                # Logs require both log_group_id and log_id
                # We need to find which log group contains this log
                log_groups = client.list_log_groups(self.compartment_id).data
                log_found = False
                for log_group in log_groups:
                    try:
                        logs = client.list_logs(log_group.id).data
                        for log in logs:
                            if log.id == resource_id:
                                client.delete_log(log_group.id, resource_id)
                                log_found = True
                                break
                        if log_found:
                            break
                    except Exception:
                        continue
                if not log_found:
                    logger.warning(f"Could not find log group for log {resource_id}")
                    raise Exception(f"Log group not found for log {resource_id}")
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
                logger.info(f"Resource already deleted or not found: {resource_name}")
                self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleted')
                return True
            elif e.status == 409:  # Conflict - usually dependency issue
                error_msg = str(e.message)
                # Check if this is a "default" resource that will be auto-deleted with VCN
                if 'is the default for VCN' in error_msg:
                    logger.info(f"Skipping default resource (will be auto-deleted with VCN): {resource_name}")
                    self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleted')
                    self.deleted_count[resource.resource_type] += 1
                    return True
                # Check for protected resources (DNS zones attached to VCN, etc.)
                elif 'Operation not allowed on protected resource' in error_msg:
                    logger.info(f"Skipping protected resource (will be auto-deleted with parent): {resource_name}")
                    self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleted')
                    self.deleted_count[resource.resource_type] += 1
                    return True
                # Boot volume still attached - instance is still terminating
                elif 'may not be deleted while attached' in error_msg:
                    if retry_count < self.max_retries:
                        logger.warning(f"Resource still attached (waiting for parent to terminate): {resource_name}")
                        return False  # Will retry
                    else:
                        # After retries, it's likely that boot volume deletion is disabled on the instance
                        # and the volume is orphaned. Report as failed.
                        logger.error(f"Failed to delete {resource_id} (still attached after instance terminated): {e.message}")
                        self.failed_count[resource.resource_type] += 1
                        self._update_resource_status(resource_id, resource_name, resource.resource_type, 'failed', e.message)
                        return False
                elif retry_count < self.max_retries:
                    logger.warning(f"Dependency conflict deleting {resource_id}, will retry later")
                    # Don't update status yet - we'll retry
                    return False
                else:
                    logger.error(f"Failed to delete {resource_id} after {self.max_retries} retries: {e.message}")
                    self.failed_count[resource.resource_type] += 1
                    self._update_resource_status(resource_id, resource_name, resource.resource_type, 'failed', e.message)
                    return False
            elif e.status == 400:
                error_msg = str(e.message)
                # Primary IPs cannot be deleted - they're deleted with the VNIC/Instance
                if 'Cannot delete primary private IP' in error_msg:
                    logger.info(f"Skipping primary IP (will be auto-deleted with Instance): {resource_name}")
                    self._update_resource_status(resource_id, resource_name, resource.resource_type, 'deleted')
                    self.deleted_count[resource.resource_type] += 1
                    return True
                else:
                    logger.error(f"Error deleting {resource_id}: {e.message}")
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

    # Resources that must be deleted AFTER certain other resources
    # (not explicitly in dependencies, but logically required)
    DELETE_LAST = {
        'BootVolume': ['Instance'],    # Boot volumes can only be deleted after instance is terminated
        'Volume': ['Instance'],        # Volumes should be deleted after instance (if attached)
        'Vcn': ['Instance', 'LoadBalancer', 'MountTarget', 'DbSystem', 'MysqlDbSystem'],  # VCN needs all network users gone
    }

    def _get_deletion_order(self, resource_types):
        """
        Determine deletion order based on dependencies
        Returns list of resource types in order they should be deleted
        """
        # Priority order (higher priority = delete earlier)
        # Resources not in this list get medium priority
        priority_order = {
            # Delete compute/database resources first (they use networking)
            'LogAnalyticsEntity': 100,
            'Key': 98,           # Keys should be deleted before Vaults
            'PublicIp': 95,      # Reserved public IPs should be freed early
            'Instance': 90,
            'ContainerInstance': 90,
            'ClustersCluster': 88,  # OKE clusters before subnets
            'FunctionsApplication': 87,  # Functions before networking
            'DbSystem': 85,
            'MysqlDbSystem': 85,
            'AutonomousDatabase': 85,
            'LoadBalancer': 80,
            'NetworkLoadBalancer': 80,
            'MountTarget': 80,
            'Bastion': 78,       # Bastions use subnets
            'DevOpsProject': 75,
            'WebAppFirewallPolicy': 75,
            'NetworkFirewallPolicy': 74,  # Network firewall policies before networking
            'EmailSender': 73,            # Email senders can be deleted early
            'HttpMonitor': 72,            # Health checks can be deleted early
            'PingMonitor': 72,
            'DISWorkspace': 71,           # Data Integration workspace before networking
            # Then storage/data resources (after instances release them)
            'Stream': 70,
            'StreamPool': 69,
            'VolumeGroup': 69,    # VolumeGroup before Volumes
            'BootVolume': 68,
            'Volume': 68,
            'VolumeBackup': 67,           # Backups before volumes
            'BootVolumeBackup': 67,
            'NoSQLTable': 66,
            'Bucket': 65,
            'ContainerRepo': 65,
            'GenericRepository': 65,      # Artifact repository
            'Snapshot': 64,               # File system snapshots before file systems
            'Export': 63,                 # Exports before file systems
            'FileSystem': 62,
            'Vault': 61,                  # After Keys
            # Then networking resources
            'LocalPeeringGateway': 55,
            'Drg': 52,
            'Subnet': 50,
            'Vlan': 48,          # VLANs are similar to subnets
            'NatGateway': 45,
            'InternetGateway': 45,
            'ServiceGateway': 45,
            'NetworkSecurityGroup': 42,
            'RouteTable': 40,
            'SecurityList': 40,
            'DHCPOptions': 35,
            'DnsZone': 30,
            'Vcn': 10,  # VCN should be deleted last
        }

        def get_priority(rtype):
            return priority_order.get(rtype, 60)  # Default medium priority

        # Sort by priority (highest first)
        return sorted(resource_types, key=get_priority, reverse=True)

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
