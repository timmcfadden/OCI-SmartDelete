#!/usr/bin/env python3
"""
Comprehensive OCI Resource Type Mapper

This creates a complete resource mapping by combining:
1. OCI SDK introspection
2. Known resource patterns from OCI-SuperDelete and ociextirpater
3. OCI service documentation patterns

Usage:
    python3 generate_comprehensive_mappings.py
"""

import oci
import inspect


def generate_comprehensive_mappings():
    """Generate comprehensive resource type mappings"""

    # Define all known OCI service clients and their resource types
    # This is based on OCI SDK documentation and common patterns

    mappings = {
        # Compute
        'Instance': {
            'client': 'compute.ComputeClient',
            'method': 'terminate_instance',
            'composite': 'compute.ComputeClientCompositeOperations',
            'composite_method': 'terminate_instance_and_wait_for_state',
            'wait_states': ['TERMINATED'],
        },
        'Image': {
            'client': 'compute.ComputeClient',
            'method': 'delete_image',
            'composite': 'compute.ComputeClientCompositeOperations',
            'composite_method': 'delete_image_and_wait_for_state',
            'wait_states': ['DELETED'],
        },
        'BootVolumeAttachment': {
            'client': 'compute.ComputeClient',
            'method': 'detach_boot_volume',
        },
        'VolumeAttachment': {
            'client': 'compute.ComputeClient',
            'method': 'detach_volume',
        },
        'InstanceConfiguration': {
            'client': 'compute_management.ComputeManagementClient',
            'method': 'delete_instance_configuration',
        },
        'InstancePool': {
            'client': 'compute_management.ComputeManagementClient',
            'method': 'terminate_instance_pool',
        },
        'ClusterNetwork': {
            'client': 'compute_management.ComputeManagementClient',
            'method': 'terminate_cluster_network',
        },
        'AutoScalingConfiguration': {
            'client': 'autoscaling.AutoScalingClient',
            'method': 'delete_auto_scaling_configuration',
        },
        'DedicatedVmHost': {
            'client': 'compute.ComputeClient',
            'method': 'delete_dedicated_vm_host',
        },
        'ConsoleHistory': {
            'client': 'compute.ComputeClient',
            'method': 'delete_console_history',
        },

        # Block Storage
        'Volume': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_volume',
            'composite': 'core.BlockstorageClientCompositeOperations',
            'composite_method': 'delete_volume_and_wait_for_state',
            'wait_states': ['TERMINATED'],
        },
        'BootVolume': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_boot_volume',
            'composite': 'core.BlockstorageClientCompositeOperations',
            'composite_method': 'delete_boot_volume_and_wait_for_state',
            'wait_states': ['TERMINATED'],
        },
        'VolumeBackup': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_volume_backup',
        },
        'BootVolumeBackup': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_boot_volume_backup',
        },
        'VolumeGroup': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_volume_group',
        },
        'VolumeGroupBackup': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_volume_group_backup',
        },
        'VolumeBackupPolicy': {
            'client': 'core.BlockstorageClient',
            'method': 'delete_volume_backup_policy',
        },

        # Networking - VCN
        'Vcn': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_vcn',
            'dependencies': ['Subnet', 'InternetGateway', 'NatGateway', 'ServiceGateway', 'RouteTable', 'SecurityList', 'LocalPeeringGateway'],
        },
        'Subnet': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_subnet',
        },
        'InternetGateway': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_internet_gateway',
        },
        'NatGateway': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_nat_gateway',
        },
        'ServiceGateway': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_service_gateway',
        },
        'RouteTable': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_route_table',
        },
        'SecurityList': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_security_list',
        },
        'DHCPOptions': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_dhcp_options',
        },
        'LocalPeeringGateway': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_local_peering_gateway',
        },
        'Drg': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_drg',
        },
        'DrgAttachment': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_drg_attachment',
        },
        'DrgRouteTable': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_drg_route_table',
        },
        'DrgRouteDistribution': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_drg_route_distribution',
        },
        'RemotePeeringConnection': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_remote_peering_connection',
        },
        'Cpe': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_cpe',
        },
        'IPSecConnection': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_ip_sec_connection',
        },
        'PublicIp': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_public_ip',
        },
        'PrivateIp': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_private_ip',
        },
        'NetworkSecurityGroup': {
            'client': 'core.VirtualNetworkClient',
            'method': 'delete_network_security_group',
        },

        # Load Balancer
        'LoadBalancer': {
            'client': 'load_balancer.LoadBalancerClient',
            'method': 'delete_load_balancer',
        },
        'NetworkLoadBalancer': {
            'client': 'network_load_balancer.NetworkLoadBalancerClient',
            'method': 'delete_network_load_balancer',
        },

        # Database
        'DbSystem': {
            'client': 'database.DatabaseClient',
            'method': 'terminate_db_system',
        },
        'AutonomousDatabase': {
            'client': 'database.DatabaseClient',
            'method': 'delete_autonomous_database',
        },
        'AutonomousContainerDatabase': {
            'client': 'database.DatabaseClient',
            'method': 'terminate_autonomous_container_database',
        },
        'AutonomousExadataInfrastructure': {
            'client': 'database.DatabaseClient',
            'method': 'terminate_autonomous_exadata_infrastructure',
        },
        'BackupDestination': {
            'client': 'database.DatabaseClient',
            'method': 'delete_backup_destination',
        },
        'DbHome': {
            'client': 'database.DatabaseClient',
            'method': 'delete_db_home',
        },
        'ExadataInfrastructure': {
            'client': 'database.DatabaseClient',
            'method': 'delete_exadata_infrastructure',
        },
        'VmCluster': {
            'client': 'database.DatabaseClient',
            'method': 'delete_vm_cluster',
        },
        'VmClusterNetwork': {
            'client': 'database.DatabaseClient',
            'method': 'delete_vm_cluster_network',
        },
        'CloudExadataInfrastructure': {
            'client': 'database.DatabaseClient',
            'method': 'delete_cloud_exadata_infrastructure',
        },
        'CloudVmCluster': {
            'client': 'database.DatabaseClient',
            'method': 'delete_cloud_vm_cluster',
        },

        # MySQL
        'MysqlDbSystem': {
            'client': 'mysql.DbSystemClient',
            'method': 'delete_db_system',
        },
        'MysqlBackup': {
            'client': 'mysql.DbBackupsClient',
            'method': 'delete_backup',
        },
        'MysqlChannel': {
            'client': 'mysql.ChannelsClient',
            'method': 'delete_channel',
        },

        # PostgreSQL
        'PostgresqlDbSystem': {
            'client': 'psql.PostgresqlClient',
            'method': 'delete_db_system',
        },
        'PostgresqlBackup': {
            'client': 'psql.PostgresqlClient',
            'method': 'delete_backup',
        },

        # NoSQL
        'NoSqlTable': {
            'client': 'nosql.NosqlClient',
            'method': 'delete_table',
        },

        # Object Storage
        'Bucket': {
            'client': 'object_storage.ObjectStorageClient',
            'method': 'delete_bucket',
            'special': 'bucket',
        },
        'PreauthenticatedRequest': {
            'client': 'object_storage.ObjectStorageClient',
            'method': 'delete_preauthenticated_request',
            'special': 'bucket',
        },

        # File Storage
        'FileSystem': {
            'client': 'file_storage.FileStorageClient',
            'method': 'delete_file_system',
        },
        'MountTarget': {
            'client': 'file_storage.FileStorageClient',
            'method': 'delete_mount_target',
        },
        'Export': {
            'client': 'file_storage.FileStorageClient',
            'method': 'delete_export',
        },
        'ExportSet': {
            'client': 'file_storage.FileStorageClient',
            'method': 'delete_export_set',
        },
        'Replication': {
            'client': 'file_storage.FileStorageClient',
            'method': 'delete_replication',
        },
        'FssReplicationTarget': {
            'client': 'file_storage.FileStorageClient',
            'method': 'delete_replication_target',
        },

        # Container Engine (OKE)
        'Cluster': {
            'client': 'container_engine.ContainerEngineClient',
            'method': 'delete_cluster',
        },
        'NodePool': {
            'client': 'container_engine.ContainerEngineClient',
            'method': 'delete_node_pool',
        },

        # Container Instances
        'ContainerInstance': {
            'client': 'container_instances.ContainerInstanceClient',
            'method': 'delete_container_instance',
        },

        # Functions
        'Function': {
            'client': 'functions.FunctionsManagementClient',
            'method': 'delete_function',
        },
        'Application': {
            'client': 'functions.FunctionsManagementClient',
            'method': 'delete_application',
            'dependencies': ['Function'],
        },

        # API Gateway
        'ApiGateway': {
            'client': 'apigateway.GatewayClient',
            'method': 'delete_gateway',
        },
        'ApiDeployment': {
            'client': 'apigateway.DeploymentClient',
            'method': 'delete_deployment',
        },
        'Api': {
            'client': 'apigateway.ApiClient',
            'method': 'delete_api',
        },

        # Events
        'EventsRule': {
            'client': 'events.EventsClient',
            'method': 'delete_rule',
        },

        # Streaming
        'Stream': {
            'client': 'streaming.StreamAdminClient',
            'method': 'delete_stream',
        },
        'StreamPool': {
            'client': 'streaming.StreamAdminClient',
            'method': 'delete_stream_pool',
        },
        'ConnectHarness': {
            'client': 'streaming.StreamAdminClient',
            'method': 'delete_connect_harness',
        },

        # Monitoring & Observability
        'Alarm': {
            'client': 'monitoring.MonitoringClient',
            'method': 'delete_alarm',
        },
        'LogGroup': {
            'client': 'logging.LoggingManagementClient',
            'method': 'delete_log_group',
        },
        'Log': {
            'client': 'logging.LoggingManagementClient',
            'method': 'delete_log',
        },
        'ServiceConnector': {
            'client': 'sch.ServiceConnectorClient',
            'method': 'delete_service_connector',
        },

        # Log Analytics
        'LogAnalyticsEntity': {
            'client': 'log_analytics.LogAnalyticsClient',
            'method': 'delete_log_analytics_entity',
        },
        'LogAnalyticsLogGroup': {
            'client': 'log_analytics.LogAnalyticsClient',
            'method': 'delete_log_analytics_log_group',
        },

        # Notifications
        'OnsTopic': {
            'client': 'ons.NotificationControlPlaneClient',
            'method': 'delete_topic',
        },
        'OnsSubscription': {
            'client': 'ons.NotificationDataPlaneClient',
            'method': 'delete_subscription',
        },

        # Cloud Guard
        'CloudGuardTarget': {
            'client': 'cloud_guard.CloudGuardClient',
            'method': 'delete_target',
        },
        'CloudGuardDetectorRecipe': {
            'client': 'cloud_guard.CloudGuardClient',
            'method': 'delete_detector_recipe',
        },
        'CloudGuardResponderRecipe': {
            'client': 'cloud_guard.CloudGuardClient',
            'method': 'delete_responder_recipe',
        },
        'CloudGuardManagedList': {
            'client': 'cloud_guard.CloudGuardClient',
            'method': 'delete_managed_list',
        },

        # Bastion
        'Bastion': {
            'client': 'bastion.BastionClient',
            'method': 'delete_bastion',
        },

        # DNS
        'CustomerDnsZone': {
            'client': 'dns.DnsClient',
            'method': 'delete_zone',
        },
        'DnsView': {
            'client': 'dns.DnsClient',
            'method': 'delete_view',
        },
        'SteeringPolicy': {
            'client': 'dns.DnsClient',
            'method': 'delete_steering_policy',
        },
        'SteeringPolicyAttachment': {
            'client': 'dns.DnsClient',
            'method': 'delete_steering_policy_attachment',
        },
        'TsigKey': {
            'client': 'dns.DnsClient',
            'method': 'delete_tsig_key',
        },
        'DnsResolver': {
            'client': 'dns.DnsClient',
            'method': 'delete_resolver',
        },

        # Data Science
        'DataScienceProject': {
            'client': 'data_science.DataScienceClient',
            'method': 'delete_project',
        },
        'DataScienceModel': {
            'client': 'data_science.DataScienceClient',
            'method': 'delete_model',
        },
        'DataScienceNotebookSession': {
            'client': 'data_science.DataScienceClient',
            'method': 'delete_notebook_session',
        },
        'DataScienceModelDeployment': {
            'client': 'data_science.DataScienceClient',
            'method': 'delete_model_deployment',
        },

        # Data Integration
        'DisWorkspace': {
            'client': 'data_integration.DataIntegrationClient',
            'method': 'delete_workspace',
        },

        # Data Catalog
        'DataCatalog': {
            'client': 'data_catalog.DataCatalogClient',
            'method': 'delete_catalog',
        },

        # Analytics
        'AnalyticsInstance': {
            'client': 'analytics.AnalyticsClient',
            'method': 'delete_analytics_instance',
        },

        # Integration
        'IntegrationInstance': {
            'client': 'integration.IntegrationInstanceClient',
            'method': 'delete_integration_instance',
        },

        # Visual Builder
        'VbInstance': {
            'client': 'visual_builder.VbInstanceClient',
            'method': 'delete_vb_instance',
        },

        # DevOps
        'DevopsProject': {
            'client': 'devops.DevopsClient',
            'method': 'delete_project',
        },
        'DevopsRepository': {
            'client': 'devops.DevopsClient',
            'method': 'delete_repository',
        },
        'BuildPipeline': {
            'client': 'devops.DevopsClient',
            'method': 'delete_build_pipeline',
        },
        'DeployPipeline': {
            'client': 'devops.DevopsClient',
            'method': 'delete_deployment_pipeline',
        },

        # Resource Manager
        'OrmStack': {
            'client': 'resource_manager.ResourceManagerClient',
            'method': 'delete_stack',
        },
        'ConfigurationSourceProvider': {
            'client': 'resource_manager.ResourceManagerClient',
            'method': 'delete_configuration_source_provider',
        },

        # Vault & Keys
        'Vault': {
            'client': 'key_management.KmsVaultClient',
            'method': 'schedule_vault_deletion',
            'special': 'vault',
        },
        'Key': {
            'client': 'key_management.KmsManagementClient',
            'method': 'schedule_key_deletion',
            'special': 'key',
        },

        # IAM
        'User': {
            'client': 'identity.IdentityClient',
            'method': 'delete_user',
        },
        'Group': {
            'client': 'identity.IdentityClient',
            'method': 'delete_group',
        },
        'DynamicResourceGroup': {
            'client': 'identity.IdentityClient',
            'method': 'delete_dynamic_group',
        },
        'Policy': {
            'client': 'identity.IdentityClient',
            'method': 'delete_policy',
        },
        'Compartment': {
            'client': 'identity.IdentityClient',
            'method': 'delete_compartment',
            'special': 'compartment',
        },
        'IdentityProvider': {
            'client': 'identity.IdentityClient',
            'method': 'delete_identity_provider',
        },
        'NetworkSource': {
            'client': 'identity.IdentityClient',
            'method': 'delete_network_source',
        },

        # GoldenGate
        'GoldenGateDeployment': {
            'client': 'golden_gate.GoldenGateClient',
            'method': 'delete_deployment',
        },
        'GoldenGateDatabaseRegistration': {
            'client': 'golden_gate.GoldenGateClient',
            'method': 'delete_database_registration',
        },

        # OpenSearch
        'OpensearchCluster': {
            'client': 'opensearch.OpensearchClusterClient',
            'method': 'delete_opensearch_cluster',
        },

        # Redis
        'RedisCluster': {
            'client': 'redis.RedisClusterClient',
            'method': 'delete_redis_cluster',
        },

        # Certificates
        'Certificate': {
            'client': 'certificates_management.CertificatesManagementClient',
            'method': 'schedule_certificate_deletion',
        },
        'CertificateAuthority': {
            'client': 'certificates_management.CertificatesManagementClient',
            'method': 'schedule_certificate_authority_deletion',
        },
    }

    # Add id_field to all (default is 'id')
    for resource_type, config in mappings.items():
        if 'id_field' not in config:
            config['id_field'] = 'id'

    return mappings


def generate_python_file(mappings, output_file):
    """Generate Python file with mappings"""

    code = '''"""
Auto-generated comprehensive OCI Resource Type Mappings

This file contains deletion configurations for all major OCI resource types.
Generated by generate_comprehensive_mappings.py

Each resource type includes:
- client: The OCI SDK client class path
- method: The deletion method name
- id_field: The field name for resource ID
- composite: (optional) Composite client for wait operations
- composite_method: (optional) Method for wait operations
- wait_states: (optional) States to wait for
- dependencies: (optional) Resources that must be deleted first
- special: (optional) Special handling required
"""

RESOURCE_TYPE_MAP = {
'''

    for resource_type in sorted(mappings.keys()):
        config = mappings[resource_type]
        code += f"    '{resource_type}': {{\n"
        code += f"        'client': '{config['client']}',\n"
        code += f"        'method': '{config['method']}',\n"
        code += f"        'id_field': '{config['id_field']}',\n"

        if 'composite' in config:
            code += f"        'composite': '{config['composite']}',\n"
            code += f"        'composite_method': '{config['composite_method']}',\n"
            code += f"        'wait_states': {config['wait_states']},\n"

        if 'dependencies' in config:
            code += f"        'dependencies': {config['dependencies']},\n"

        if 'special' in config:
            code += f"        'special': '{config['special']}',\n"

        code += "    },\n"

    code += "}\n"

    with open(output_file, 'w') as f:
        f.write(code)

    print(f"✓ Generated {output_file}")
    print(f"  Total resource types: {len(mappings)}")


if __name__ == '__main__':
    print("Generating comprehensive OCI resource type mappings...")
    print("="*80)

    mappings = generate_comprehensive_mappings()

    generate_python_file(mappings, 'oci_resource_types.py')

    print("\n" + "="*80)
    print("Resource Types by Category:")
    print("="*80)

    # Group by service
    by_service = {}
    for rtype, config in mappings.items():
        service = config['client'].split('.')[0]
        if service not in by_service:
            by_service[service] = []
        by_service[service].append(rtype)

    for service in sorted(by_service.keys()):
        print(f"\n{service.upper()}: {len(by_service[service])} types")
        for rtype in sorted(by_service[service])[:5]:
            print(f"  - {rtype}")
        if len(by_service[service]) > 5:
            print(f"  ... and {len(by_service[service]) - 5} more")

    print("\n" + "="*80)
    print("Next step: Update oci_smart_delete.py to import from oci_resource_types.py")
