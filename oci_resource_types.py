"""
Comprehensive OCI Resource Type Mappings

This file contains deletion configurations for OCI resource types.
Auto-generated and manually verified against the OCI SDK.

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
    'AiDocumentModel': {
        'client': 'ai_document.AIServiceDocumentClient',
        'method': 'delete_model',
        'id_field': 'id',
    },
    'AiDocumentProject': {
        'client': 'ai_document.AIServiceDocumentClient',
        'method': 'delete_project',
        'id_field': 'id',
    },
    'AiLanguageEndpoint': {
        'client': 'ai_language.AIServiceLanguageClient',
        'method': 'delete_endpoint',
        'id_field': 'id',
    },
    'AiLanguageModel': {
        'client': 'ai_language.AIServiceLanguageClient',
        'method': 'delete_model',
        'id_field': 'id',
    },
    'AiLanguageProject': {
        'client': 'ai_language.AIServiceLanguageClient',
        'method': 'delete_project',
        'id_field': 'id',
    },
    'AiModel': {
        'client': 'ai_vision.AIServiceVisionClient',
        'method': 'delete_model',
        'id_field': 'id',
    },
    'AiModelDeployment': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_model_deployment',
        'id_field': 'id',
    },
    'AiProject': {
        'client': 'ai_vision.AIServiceVisionClient',
        'method': 'delete_project',
        'id_field': 'id',
    },
    'AiVisionModel': {
        'client': 'ai_vision.AIServiceVisionClient',
        'method': 'delete_model',
        'id_field': 'id',
    },
    'AiVisionProject': {
        'client': 'ai_vision.AIServiceVisionClient',
        'method': 'delete_project',
        'id_field': 'id',
    },
    'Alarm': {
        'client': 'monitoring.MonitoringClient',
        'method': 'delete_alarm',
        'id_field': 'id',
    },
    'AnalyticsInstance': {
        'client': 'analytics.AnalyticsClient',
        'method': 'delete_analytics_instance',
        'id_field': 'id',
    },
    'Api': {
        'client': 'apigateway.ApiGatewayClient',
        'method': 'delete_api',
        'id_field': 'api_id',
    },
    'ApiDeployment': {
        'client': 'apigateway.DeploymentClient',
        'method': 'delete_deployment',
        'id_field': 'id',
    },
    'ApiGateway': {
        'client': 'apigateway.GatewayClient',
        'method': 'delete_gateway',
        'id_field': 'id',
    },
    'ApiGatewayApi': {
        'client': 'apigateway.ApiGatewayClient',
        'method': 'delete_api',
        'id_field': 'api_id',
    },
    'ApiGatewayCertificate': {
        'client': 'apigateway.ApiGatewayClient',
        'method': 'delete_certificate',
        'id_field': 'id',
    },
    'ApiGatewaySdk': {
        'client': 'apigateway.ApiGatewayClient',
        'method': 'delete_sdk',
        'id_field': 'id',
    },
    'ApiGatewaySubscriber': {
        'client': 'apigateway.SubscribersClient',
        'method': 'delete_subscriber',
        'id_field': 'id',
    },
    'ApiGatewayUsagePlan': {
        'client': 'apigateway.UsagePlansClient',
        'method': 'delete_usage_plan',
        'id_field': 'id',
    },
    'ApiPlatformInstance': {
        'client': 'api_platform.ApiPlatformClient',
        'method': 'delete_api_platform_instance',
        'id_field': 'id',
    },
    'ApmDomain': {
        'client': 'apm_control_plane.ApmDomainClient',
        'method': 'delete_apm_domain',
        'id_field': 'apm_domain_id',
    },
    'Application': {
        'client': 'functions.FunctionsManagementClient',
        'method': 'delete_application',
        'id_field': 'id',
        'dependencies': ['Function'],
    },
    'ApplicationVip': {
        'client': 'database.DatabaseClient',
        'method': 'delete_application_vip',
        'id_field': 'id',
    },
    'AutoScalingConfiguration': {
        'client': 'autoscaling.AutoScalingClient',
        'method': 'delete_auto_scaling_configuration',
        'id_field': 'id',
    },
    'AutonomousContainerDatabase': {
        'client': 'database.DatabaseClient',
        'method': 'terminate_autonomous_container_database',
        'id_field': 'id',
    },
    'AutonomousDatabase': {
        'client': 'database.DatabaseClient',
        'method': 'delete_autonomous_database',
        'id_field': 'id',
    },
    'AutonomousDatabaseBackup': {
        'client': 'database.DatabaseClient',
        'method': 'delete_autonomous_database_backup',
        'id_field': 'id',
    },
    'AutonomousDatabaseSoftwareImage': {
        'client': 'database.DatabaseClient',
        'method': 'delete_autonomous_database_software_image',
        'id_field': 'id',
    },
    'AutonomousExadataInfrastructure': {
        'client': 'database.DatabaseClient',
        'method': 'terminate_autonomous_exadata_infrastructure',
        'id_field': 'id',
    },
    'AutonomousVmCluster': {
        'client': 'database.DatabaseClient',
        'method': 'delete_autonomous_vm_cluster',
        'id_field': 'id',
    },
    'BackupDestination': {
        'client': 'database.DatabaseClient',
        'method': 'delete_backup_destination',
        'id_field': 'id',
    },
    'Bastion': {
        'client': 'bastion.BastionClient',
        'method': 'delete_bastion',
        'id_field': 'id',
    },
    'BigDataService': {
        'client': 'bds.BdsClient',
        'method': 'delete_bds_instance',
        'id_field': 'id',
    },
    'BlockchainPlatform': {
        'client': 'blockchain.BlockchainPlatformClient',
        'method': 'delete_blockchain_platform',
        'id_field': 'id',
    },
    'BootVolume': {
        'client': 'core.BlockstorageClient',
        'method': 'delete_boot_volume',
        'id_field': 'id',
        'composite': 'core.BlockstorageClientCompositeOperations',
        'composite_method': 'delete_boot_volume_and_wait_for_state',
        'wait_states': ['TERMINATED'],
    },
    'BootVolumeAttachment': {
        'client': 'core.ComputeClient',
        'method': 'detach_boot_volume',
        'id_field': 'id',
    },
    'BootVolumeBackup': {
        'client': 'core.BlockstorageClient',
        'method': 'delete_boot_volume_backup',
        'id_field': 'id',
    },
    'Bucket': {
        'client': 'object_storage.ObjectStorageClient',
        'method': 'delete_bucket',
        'id_field': 'id',
        'special': 'bucket',
    },
    'Budget': {
        'client': 'budget.BudgetClient',
        'method': 'delete_budget',
        'id_field': 'id',
    },
    'BuildPipeline': {
        'client': 'devops.DevopsClient',
        'method': 'delete_build_pipeline',
        'id_field': 'id',
    },
    'Byoasn': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_byoasn',
        'id_field': 'id',
    },
    'ByoipRange': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_byoip_range',
        'id_field': 'id',
    },
    'CaBundle': {
        'client': 'certificates_management.CertificatesManagementClient',
        'method': 'delete_ca_bundle',
        'id_field': 'id',
    },
    'CccInfrastructure': {
        'client': 'compute_cloud_at_customer.ComputeCloudAtCustomerClient',
        'method': 'delete_ccc_infrastructure',
        'id_field': 'id',
    },
    'CccUpgradeSchedule': {
        'client': 'compute_cloud_at_customer.ComputeCloudAtCustomerClient',
        'method': 'delete_ccc_upgrade_schedule',
        'id_field': 'id',
    },
    'Certificate': {
        'client': 'certificates_management.CertificatesManagementClient',
        'method': 'schedule_certificate_deletion',
        'id_field': 'id',
    },
    'CertificateAuthority': {
        'client': 'certificates_management.CertificatesManagementClient',
        'method': 'schedule_certificate_authority_deletion',
        'id_field': 'id',
    },
    'CloudAutonomousVmCluster': {
        'client': 'database.DatabaseClient',
        'method': 'delete_cloud_autonomous_vm_cluster',
        'id_field': 'id',
    },
    'CloudExadataInfrastructure': {
        'client': 'database.DatabaseClient',
        'method': 'delete_cloud_exadata_infrastructure',
        'id_field': 'id',
    },
    'CloudGuardAdhocQuery': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_adhoc_query',
        'id_field': 'id',
    },
    'CloudGuardDataSource': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_data_source',
        'id_field': 'id',
    },
    'CloudGuardDetectorRecipe': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_detector_recipe',
        'id_field': 'id',
    },
    'CloudGuardManagedList': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_managed_list',
        'id_field': 'id',
    },
    'CloudGuardResponderRecipe': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_responder_recipe',
        'id_field': 'id',
    },
    'CloudGuardSavedQuery': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_saved_query',
        'id_field': 'id',
    },
    'CloudGuardTarget': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_target',
        'id_field': 'id',
    },
    'CloudVmCluster': {
        'client': 'database.DatabaseClient',
        'method': 'delete_cloud_vm_cluster',
        'id_field': 'id',
    },
    'Cluster': {
        'client': 'container_engine.ContainerEngineClient',
        'method': 'delete_cluster',
        'id_field': 'id',
    },
    'ClusterNetwork': {
        'client': 'core.ComputeManagementClient',
        'method': 'terminate_cluster_network',
        'id_field': 'id',
    },
    'ClusterPlacementGroup': {
        'client': 'cluster_placement_groups.ClusterPlacementGroupsCPClient',
        'method': 'delete_cluster_placement_group',
        'id_field': 'id',
    },
    'ClustersCluster': {
        'client': 'container_engine.ContainerEngineClient',
        'method': 'delete_cluster',
        'id_field': 'id',
    },
    'Compartment': {
        'client': 'identity.IdentityClient',
        'method': 'delete_compartment',
        'id_field': 'id',
        'special': 'compartment',
    },
    'ComputeCapacityReservation': {
        'client': 'core.ComputeClient',
        'method': 'delete_compute_capacity_reservation',
        'id_field': 'id',
    },
    'ConfigurationSourceProvider': {
        'client': 'resource_manager.ResourceManagerClient',
        'method': 'delete_configuration_source_provider',
        'id_field': 'id',
    },
    'ConnectHarness': {
        'client': 'streaming.StreamAdminClient',
        'method': 'delete_connect_harness',
        'id_field': 'id',
    },
    'ConsoleHistory': {
        'client': 'core.ComputeClient',
        'method': 'delete_console_history',
        'id_field': 'id',
    },
    'ContainerImage': {
        'client': 'artifacts.ArtifactsClient',
        'method': 'delete_container_image',
        'id_field': 'id',
    },
    'ContainerInstance': {
        'client': 'container_instances.ContainerInstanceClient',
        'method': 'delete_container_instance',
        'id_field': 'id',
    },
    'ContainerRepo': {
        'client': 'artifacts.ArtifactsClient',
        'method': 'delete_container_repository',
        'id_field': 'id',
    },
    'Cpe': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_cpe',
        'id_field': 'id',
    },
    'CrossConnect': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_cross_connect',
        'id_field': 'id',
    },
    'CrossConnectGroup': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_cross_connect_group',
        'id_field': 'id',
    },
    'CustomerDnsZone': {
        'client': 'dns.DnsClient',
        'method': 'delete_zone',
        'id_field': 'id',
    },
    'DHCPOptions': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_dhcp_options',
        'id_field': 'id',
    },
    'DISWorkspace': {
        'client': 'data_integration.DataIntegrationClient',
        'method': 'delete_workspace',
        'id_field': 'id',
    },
    'DataCatalog': {
        'client': 'data_catalog.DataCatalogClient',
        'method': 'delete_catalog',
        'id_field': 'id',
    },
    'DataCatalogMetastore': {
        'client': 'data_catalog.DataCatalogClient',
        'method': 'delete_metastore',
        'id_field': 'id',
    },
    'DataCatalogPrivateEndpoint': {
        'client': 'data_catalog.DataCatalogClient',
        'method': 'delete_catalog_private_endpoint',
        'id_field': 'id',
    },
    'DataFlowApplication': {
        'client': 'data_flow.DataFlowClient',
        'method': 'delete_application',
        'id_field': 'id',
    },
    'DataFlowPool': {
        'client': 'data_flow.DataFlowClient',
        'method': 'delete_pool',
        'id_field': 'id',
    },
    'DataFlowRun': {
        'client': 'data_flow.DataFlowClient',
        'method': 'delete_run',
        'id_field': 'id',
    },
    'DataFlowSqlEndpoint': {
        'client': 'data_flow.DataFlowClient',
        'method': 'delete_sql_endpoint',
        'id_field': 'id',
    },
    'DataLabelingDataset': {
        'client': 'data_labeling_service.DataLabelingManagementClient',
        'method': 'delete_dataset',
        'id_field': 'id',
    },
    'DataSafeAlertPolicy': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_alert_policy',
        'id_field': 'id',
    },
    'DataSafeAuditProfile': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_audit_profile',
        'id_field': 'id',
    },
    'DataSafeAuditTrail': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_audit_trail',
        'id_field': 'id',
    },
    'DataSafeDiscoveryJob': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_discovery_job',
        'id_field': 'id',
    },
    'DataSafeLibraryMaskingFormat': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_library_masking_format',
        'id_field': 'id',
    },
    'DataSafeMaskingPolicy': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_masking_policy',
        'id_field': 'id',
    },
    'DataSafeOnpremConnector': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_on_prem_connector',
        'id_field': 'id',
    },
    'DataSafePrivateEndpoint': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_data_safe_private_endpoint',
        'id_field': 'id',
    },
    'DataSafeReportDefinition': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_report_definition',
        'id_field': 'id',
    },
    'DataSafeSdmMaskingPolicyDifference': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_sdm_masking_policy_difference',
        'id_field': 'id',
    },
    'DataSafeSecurityAssessment': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_security_assessment',
        'id_field': 'id',
    },
    'DataSafeSensitiveDataModel': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_sensitive_data_model',
        'id_field': 'id',
    },
    'DataSafeSensitiveType': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_sensitive_type',
        'id_field': 'id',
    },
    'DataSafeSqlCollection': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_sql_collection',
        'id_field': 'id',
    },
    'DataSafeSqlFirewallPolicy': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_sql_firewall_policy',
        'id_field': 'id',
    },
    'DataSafeTargetDatabase': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_target_database',
        'id_field': 'id',
    },
    'DataSafeUserAssessment': {
        'client': 'data_safe.DataSafeClient',
        'method': 'delete_user_assessment',
        'id_field': 'id',
    },
    'DataScienceJob': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_job',
        'id_field': 'id',
    },
    'DataScienceJobRun': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_job_run',
        'id_field': 'id',
    },
    'DataScienceModel': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_model',
        'id_field': 'id',
    },
    'DataScienceModelDeployment': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_model_deployment',
        'id_field': 'id',
    },
    'DataScienceModelVersionSet': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_model_version_set',
        'id_field': 'id',
    },
    'DataScienceNotebookSession': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_notebook_session',
        'id_field': 'id',
    },
    'DataSciencePipeline': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_pipeline',
        'id_field': 'id',
    },
    'DataSciencePipelineRun': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_pipeline_run',
        'id_field': 'id',
    },
    'DataSciencePrivateEndpoint': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_data_science_private_endpoint',
        'id_field': 'id',
    },
    'DataScienceProject': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_project',
        'id_field': 'id',
    },
    'DataScienceSchedule': {
        'client': 'data_science.DataScienceClient',
        'method': 'delete_schedule',
        'id_field': 'id',
    },
    'Database': {
        'client': 'database.DatabaseClient',
        'method': 'delete_database',
        'id_field': 'id',
    },
    'DatabaseSoftwareImage': {
        'client': 'database.DatabaseClient',
        'method': 'delete_database_software_image',
        'id_field': 'id',
    },
    'DatabaseToolsConnection': {
        'client': 'database_tools.DatabaseToolsClient',
        'method': 'delete_database_tools_connection',
        'id_field': 'id',
    },
    'DatabaseToolsPrivateEndpoint': {
        'client': 'database_tools.DatabaseToolsClient',
        'method': 'delete_database_tools_private_endpoint',
        'id_field': 'id',
    },
    'DbHome': {
        'client': 'database.DatabaseClient',
        'method': 'delete_db_home',
        'id_field': 'id',
    },
    'DbKeyStore': {
        'client': 'database.DatabaseClient',
        'method': 'delete_key_store',
        'id_field': 'id',
    },
    'DbSystem': {
        'client': 'database.DatabaseClient',
        'method': 'terminate_db_system',
        'id_field': 'id',
    },
    'DedicatedVmHost': {
        'client': 'core.ComputeClient',
        'method': 'delete_dedicated_vm_host',
        'id_field': 'id',
    },
    'DeployPipeline': {
        'client': 'devops.DevopsClient',
        'method': 'delete_deployment_pipeline',
        'id_field': 'id',
    },
    'DesktopPool': {
        'client': 'desktops.DesktopServiceClient',
        'method': 'delete_desktop_pool',
        'id_field': 'id',
    },
    'DevOpsBuildPipeline': {
        'client': 'devops.DevopsClient',
        'method': 'delete_build_pipeline',
        'id_field': 'id',
    },
    'DevOpsBuildPipelineStage': {
        'client': 'devops.DevopsClient',
        'method': 'delete_build_pipeline_stage',
        'id_field': 'id',
    },
    'DevOpsConnection': {
        'client': 'devops.DevopsClient',
        'method': 'delete_connection',
        'id_field': 'id',
    },
    'DevOpsDeployArtifact': {
        'client': 'devops.DevopsClient',
        'method': 'delete_deploy_artifact',
        'id_field': 'id',
    },
    'DevOpsDeployEnvironment': {
        'client': 'devops.DevopsClient',
        'method': 'delete_deploy_environment',
        'id_field': 'id',
    },
    'DevOpsDeployPipeline': {
        'client': 'devops.DevopsClient',
        'method': 'delete_deploy_pipeline',
        'id_field': 'id',
    },
    'DevOpsDeployStage': {
        'client': 'devops.DevopsClient',
        'method': 'delete_deploy_stage',
        'id_field': 'id',
    },
    'DevOpsProject': {
        'client': 'devops.DevopsClient',
        'method': 'delete_project',
        'id_field': 'project_id',
        'dependencies': ['DevOpsRepository'],
    },
    'DevOpsRepository': {
        'client': 'devops.DevopsClient',
        'method': 'delete_repository',
        'id_field': 'repository_id',
    },
    'DevOpsTrigger': {
        'client': 'devops.DevopsClient',
        'method': 'delete_trigger',
        'id_field': 'id',
    },
    'DevopsProject': {
        'client': 'devops.DevopsClient',
        'method': 'delete_project',
        'id_field': 'id',
    },
    'DevopsRepository': {
        'client': 'devops.DevopsClient',
        'method': 'delete_repository',
        'id_field': 'id',
    },
    'DisWorkspace': {
        'client': 'data_integration.DataIntegrationClient',
        'method': 'delete_workspace',
        'id_field': 'id',
    },
    'DnsResolver': {
        'client': 'dns.DnsClient',
        'method': 'delete_resolver',
        'id_field': 'id',
    },
    'DnsTsigKey': {
        'client': 'dns.DnsClient',
        'method': 'delete_tsig_key',
        'id_field': 'id',
    },
    'DnsView': {
        'client': 'dns.DnsClient',
        'method': 'delete_view',
        'id_field': 'id',
    },
    'DnsZone': {
        'client': 'dns.DnsClient',
        'method': 'delete_zone',
        'id_field': 'id',
    },
    'DrPlan': {
        'client': 'disaster_recovery.DisasterRecoveryClient',
        'method': 'delete_dr_plan',
        'id_field': 'id',
    },
    'DrPlanExecution': {
        'client': 'disaster_recovery.DisasterRecoveryClient',
        'method': 'delete_dr_plan_execution',
        'id_field': 'id',
    },
    'DrProtectionGroup': {
        'client': 'disaster_recovery.DisasterRecoveryClient',
        'method': 'delete_dr_protection_group',
        'id_field': 'id',
    },
    'Drg': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_drg',
        'id_field': 'id',
    },
    'DrgAttachment': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_drg_attachment',
        'id_field': 'id',
    },
    'DrgRouteDistribution': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_drg_route_distribution',
        'id_field': 'id',
    },
    'DrgRouteTable': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_drg_route_table',
        'id_field': 'id',
    },
    'DynamicResourceGroup': {
        'client': 'identity.IdentityClient',
        'method': 'delete_dynamic_group',
        'id_field': 'id',
    },
    'EkmsPrivateEndpoint': {
        'client': 'key_management.EkmClient',
        'method': 'delete_ekms_private_endpoint',
        'id_field': 'id',
    },
    'EmailDkim': {
        'client': 'email.EmailClient',
        'method': 'delete_dkim',
        'id_field': 'id',
    },
    'EmailDomain': {
        'client': 'email.EmailClient',
        'method': 'delete_email_domain',
        'id_field': 'id',
    },
    'EmailReturnPath': {
        'client': 'email.EmailClient',
        'method': 'delete_email_return_path',
        'id_field': 'id',
    },
    'EmailSender': {
        'client': 'email.EmailClient',
        'method': 'delete_sender',
        'id_field': 'id',
    },
    'EventRule': {
        'client': 'events.EventsClient',
        'method': 'delete_rule',
        'id_field': 'id',
    },
    'EventsRule': {
        'client': 'events.EventsClient',
        'method': 'delete_rule',
        'id_field': 'id',
    },
    'ExadataInfrastructure': {
        'client': 'database.DatabaseClient',
        'method': 'delete_exadata_infrastructure',
        'id_field': 'id',
    },
    'ExadbVmCluster': {
        'client': 'database.DatabaseClient',
        'method': 'delete_exadb_vm_cluster',
        'id_field': 'id',
    },
    'ExascaleDbStorageVault': {
        'client': 'database.DatabaseClient',
        'method': 'delete_exascale_db_storage_vault',
        'id_field': 'id',
    },
    'Export': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_export',
        'id_field': 'id',
    },
    'ExportSet': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_export_set',
        'id_field': 'id',
    },
    'ExternalContainerDatabase': {
        'client': 'database.DatabaseClient',
        'method': 'delete_external_container_database',
        'id_field': 'id',
    },
    'ExternalDatabaseConnector': {
        'client': 'database.DatabaseClient',
        'method': 'delete_external_database_connector',
        'id_field': 'id',
    },
    'ExternalNonContainerDatabase': {
        'client': 'database.DatabaseClient',
        'method': 'delete_external_non_container_database',
        'id_field': 'id',
    },
    'ExternalPluggableDatabase': {
        'client': 'database.DatabaseClient',
        'method': 'delete_external_pluggable_database',
        'id_field': 'id',
    },
    'FileSystem': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_file_system',
        'id_field': 'id',
    },
    'FilesystemSnapshotPolicy': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_filesystem_snapshot_policy',
        'id_field': 'id',
    },
    'FssReplicationTarget': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_replication_target',
        'id_field': 'id',
    },
    'FsuCollection': {
        'client': 'fleet_software_update.FleetSoftwareUpdateClient',
        'method': 'delete_fsu_collection',
        'id_field': 'id',
    },
    'FsuCycle': {
        'client': 'fleet_software_update.FleetSoftwareUpdateClient',
        'method': 'delete_fsu_cycle',
        'id_field': 'id',
    },
    'FsuDiscovery': {
        'client': 'fleet_software_update.FleetSoftwareUpdateClient',
        'method': 'delete_fsu_discovery',
        'id_field': 'id',
    },
    'Function': {
        'client': 'functions.FunctionsManagementClient',
        'method': 'delete_function',
        'id_field': 'id',
    },
    'FunctionsApplication': {
        'client': 'functions.FunctionsManagementClient',
        'method': 'delete_application',
        'id_field': 'id',
    },
    'FunctionsFunction': {
        'client': 'functions.FunctionsManagementClient',
        'method': 'delete_function',
        'id_field': 'id',
    },
    'FusionEnvironment': {
        'client': 'fusion_apps.FusionApplicationsClient',
        'method': 'delete_fusion_environment',
        'id_field': 'id',
    },
    'FusionEnvironmentFamily': {
        'client': 'fusion_apps.FusionApplicationsClient',
        'method': 'delete_fusion_environment_family',
        'id_field': 'id',
    },
    'GenAiAgent': {
        'client': 'generative_ai_agent.GenerativeAiAgentClient',
        'method': 'delete_agent',
        'id_field': 'id',
    },
    'GenAiAgentDataSource': {
        'client': 'generative_ai_agent.GenerativeAiAgentClient',
        'method': 'delete_data_source',
        'id_field': 'id',
    },
    'GenAiAgentEndpoint': {
        'client': 'generative_ai_agent.GenerativeAiAgentClient',
        'method': 'delete_agent_endpoint',
        'id_field': 'id',
    },
    'GenAiAgentKnowledgeBase': {
        'client': 'generative_ai_agent.GenerativeAiAgentClient',
        'method': 'delete_knowledge_base',
        'id_field': 'id',
    },
    'GenerativeAiDedicatedAiCluster': {
        'client': 'generative_ai.GenerativeAiClient',
        'method': 'delete_dedicated_ai_cluster',
        'id_field': 'id',
    },
    'GenerativeAiEndpoint': {
        'client': 'generative_ai.GenerativeAiClient',
        'method': 'delete_endpoint',
        'id_field': 'id',
    },
    'GenerativeAiModel': {
        'client': 'generative_ai.GenerativeAiClient',
        'method': 'delete_model',
        'id_field': 'id',
    },
    'GenericRepository': {
        'client': 'artifacts.ArtifactsClient',
        'method': 'delete_repository',
        'id_field': 'id',
    },
    'GoldenGateConnection': {
        'client': 'golden_gate.GoldenGateClient',
        'method': 'delete_connection',
        'id_field': 'id',
    },
    'GoldenGateDatabaseRegistration': {
        'client': 'golden_gate.GoldenGateClient',
        'method': 'delete_database_registration',
        'id_field': 'id',
    },
    'GoldenGateDeployment': {
        'client': 'golden_gate.GoldenGateClient',
        'method': 'delete_deployment',
        'id_field': 'id',
    },
    'GoldenGateDeploymentBackup': {
        'client': 'golden_gate.GoldenGateClient',
        'method': 'delete_deployment_backup',
        'id_field': 'id',
    },
    'GoldenGatePipeline': {
        'client': 'golden_gate.GoldenGateClient',
        'method': 'delete_pipeline',
        'id_field': 'id',
    },
    'Group': {
        'client': 'identity.IdentityClient',
        'method': 'delete_group',
        'id_field': 'id',
    },
    'HttpMonitor': {
        'client': 'healthchecks.HealthChecksClient',
        'method': 'delete_http_monitor',
        'id_field': 'id',
    },
    'HttpRedirect': {
        'client': 'waas.RedirectClient',
        'method': 'delete_http_redirect',
        'id_field': 'id',
    },
    'IPSecConnection': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_ip_sec_connection',
        'id_field': 'id',
    },
    'IdentityProvider': {
        'client': 'identity.IdentityClient',
        'method': 'delete_identity_provider',
        'id_field': 'id',
    },
    'Image': {
        'client': 'core.ComputeClient',
        'method': 'delete_image',
        'id_field': 'id',
        'composite': 'core.ComputeClientCompositeOperations',
        'composite_method': 'delete_image_and_wait_for_state',
        'wait_states': ['DELETED'],
    },
    'Instance': {
        'client': 'core.ComputeClient',
        'method': 'terminate_instance',
        'id_field': 'id',
        'composite': 'core.ComputeClientCompositeOperations',
        'composite_method': 'terminate_instance_and_wait_for_state',
        'wait_states': ['TERMINATED'],
    },
    'InstanceConfiguration': {
        'client': 'core.ComputeManagementClient',
        'method': 'delete_instance_configuration',
        'id_field': 'id',
    },
    'InstancePool': {
        'client': 'core.ComputeManagementClient',
        'method': 'terminate_instance_pool',
        'id_field': 'id',
    },
    'IntegrationInstance': {
        'client': 'integration.IntegrationInstanceClient',
        'method': 'delete_integration_instance',
        'id_field': 'id',
    },
    'InternetGateway': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_internet_gateway',
        'id_field': 'id',
    },
    'InventoryAsset': {
        'client': 'cloud_bridge.InventoryClient',
        'method': 'delete_asset',
        'id_field': 'id',
    },
    'Ipv6': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_ipv6',
        'id_field': 'id',
    },
    'KafkaCluster': {
        'client': 'managed_kafka.KafkaClusterClient',
        'method': 'delete_kafka_cluster',
        'id_field': 'id',
    },
    'Key': {
        'client': 'key_management.KmsManagementClient',
        'method': 'schedule_key_deletion',
        'id_field': 'id',
        'special': 'key',
    },
    'KmsHsmCluster': {
        'client': 'key_management.KmsHsmClusterClient',
        'method': 'schedule_hsm_cluster_deletion',
        'id_field': 'id',
    },
    'LoadBalancer': {
        'client': 'load_balancer.LoadBalancerClient',
        'method': 'delete_load_balancer',
        'id_field': 'id',
    },
    'LocalPeeringGateway': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_local_peering_gateway',
        'id_field': 'id',
    },
    'Log': {
        'client': 'logging.LoggingManagementClient',
        'method': 'delete_log',
        'id_field': 'id',
        'special': 'log',
    },
    'LogAnalyticsEntity': {
        'client': 'log_analytics.LogAnalyticsClient',
        'method': 'delete_log_analytics_entity',
        'id_field': 'id',
        'special': 'log_analytics_entity',
    },
    'LogAnalyticsLogGroup': {
        'client': 'log_analytics.LogAnalyticsClient',
        'method': 'delete_log_analytics_log_group',
        'id_field': 'id',
    },
    'LogGroup': {
        'client': 'logging.LoggingManagementClient',
        'method': 'delete_log_group',
        'id_field': 'id',
    },
    'LogSavedSearch': {
        'client': 'logging.LoggingManagementClient',
        'method': 'delete_log_saved_search',
        'id_field': 'id',
    },
    'LustreFileSystem': {
        'client': 'lustre_file_storage.LustreFileStorageClient',
        'method': 'delete_lustre_file_system',
        'id_field': 'id',
    },
    'ManagementAgent': {
        'client': 'management_agent.ManagementAgentClient',
        'method': 'delete_management_agent',
        'id_field': 'id',
    },
    'ManagementAgentInstallKey': {
        'client': 'management_agent.ManagementAgentClient',
        'method': 'delete_management_agent_install_key',
        'id_field': 'id',
    },
    'MediaAsset': {
        'client': 'media_services.MediaServicesClient',
        'method': 'delete_media_asset',
        'id_field': 'id',
    },
    'MediaWorkflow': {
        'client': 'media_services.MediaServicesClient',
        'method': 'delete_media_workflow',
        'id_field': 'id',
    },
    'MediaWorkflowConfiguration': {
        'client': 'media_services.MediaServicesClient',
        'method': 'delete_media_workflow_configuration',
        'id_field': 'id',
    },
    'MediaWorkflowJob': {
        'client': 'media_services.MediaServicesClient',
        'method': 'delete_media_workflow_job',
        'id_field': 'id',
    },
    'Migration': {
        'client': 'cloud_migrations.MigrationClient',
        'method': 'delete_migration',
        'id_field': 'id',
        'dependencies': ['MigrationPlan'],
    },
    'MigrationPlan': {
        'client': 'cloud_migrations.MigrationClient',
        'method': 'delete_migration_plan',
        'id_field': 'id',
    },
    'MountTarget': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_mount_target',
        'id_field': 'id',
    },
    'MysqlBackup': {
        'client': 'mysql.DbBackupsClient',
        'method': 'delete_backup',
        'id_field': 'id',
    },
    'MysqlChannel': {
        'client': 'mysql.ChannelsClient',
        'method': 'delete_channel',
        'id_field': 'id',
    },
    'MysqlConfiguration': {
        'client': 'mysql.MysqlaasClient',
        'method': 'delete_configuration',
        'id_field': 'id',
    },
    'MysqlDbSystem': {
        'client': 'mysql.DbSystemClient',
        'method': 'delete_db_system',
        'id_field': 'id',
    },
    'MysqlReplica': {
        'client': 'mysql.ReplicasClient',
        'method': 'delete_replica',
        'id_field': 'id',
    },
    'NatGateway': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_nat_gateway',
        'id_field': 'id',
    },
    'NetworkFirewall': {
        'client': 'network_firewall.NetworkFirewallClient',
        'method': 'delete_network_firewall',
        'id_field': 'id',
    },
    'NetworkFirewallPolicy': {
        'client': 'network_firewall.NetworkFirewallClient',
        'method': 'delete_network_firewall_policy',
        'id_field': 'id',
    },
    'NetworkLoadBalancer': {
        'client': 'network_load_balancer.NetworkLoadBalancerClient',
        'method': 'delete_network_load_balancer',
        'id_field': 'id',
    },
    'NetworkSecurityGroup': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_network_security_group',
        'id_field': 'id',
    },
    'NetworkSource': {
        'client': 'identity.IdentityClient',
        'method': 'delete_network_source',
        'id_field': 'id',
    },
    'NoSQLTable': {
        'client': 'nosql.NosqlClient',
        'method': 'delete_table',
        'id_field': 'id',
    },
    'NoSqlTable': {
        'client': 'nosql.NosqlClient',
        'method': 'delete_table',
        'id_field': 'id',
    },
    'NodePool': {
        'client': 'container_engine.ContainerEngineClient',
        'method': 'delete_node_pool',
        'id_field': 'id',
    },
    'OcbAgent': {
        'client': 'cloud_bridge.OcbAgentSvcClient',
        'method': 'delete_agent',
        'id_field': 'id',
    },
    'OcbAgentDependency': {
        'client': 'cloud_bridge.OcbAgentSvcClient',
        'method': 'delete_agent_dependency',
        'id_field': 'id',
    },
    'OcbAssetSource': {
        'client': 'cloud_bridge.DiscoveryClient',
        'method': 'delete_asset_source',
        'id_field': 'id',
    },
    'OcbAwsEbsAsset': {
        'client': 'cloud_bridge.InventoryClient',
        'method': 'delete_asset',
        'id_field': 'id',
    },
    'OcbAwsEcTwoAsset': {
        'client': 'cloud_bridge.InventoryClient',
        'method': 'delete_asset',
        'id_field': 'id',
    },
    'OcbDiscoverySchedule': {
        'client': 'cloud_bridge.DiscoveryClient',
        'method': 'delete_discovery_schedule',
        'id_field': 'id',
    },
    'OcbEnvironment': {
        'client': 'cloud_bridge.OcbAgentSvcClient',
        'method': 'delete_environment',
        'id_field': 'id',
        'dependencies': ['OcbAssetSource'],
    },
    'OcbInventory': {
        'client': 'cloud_bridge.InventoryClient',
        'method': 'delete_inventory',
        'id_field': 'id',
    },
    'OcbOracleDbAsset': {
        'client': 'cloud_bridge.InventoryClient',
        'method': 'delete_asset',
        'id_field': 'id',
    },
    'OcbVmAsset': {
        'client': 'cloud_bridge.InventoryClient',
        'method': 'delete_asset',
        'id_field': 'id',
    },
    'OcbVmwareVmAsset': {
        'client': 'cloud_bridge.InventoryClient',
        'method': 'delete_asset',
        'id_field': 'id',
    },
    'OccAvailabilityCatalog': {
        'client': 'capacity_management.CapacityManagementClient',
        'method': 'delete_occ_availability_catalog',
        'id_field': 'id',
    },
    'OccCapacityRequest': {
        'client': 'capacity_management.CapacityManagementClient',
        'method': 'delete_occ_capacity_request',
        'id_field': 'id',
    },
    'OceInstance': {
        'client': 'oce.OceInstanceClient',
        'method': 'delete_oce_instance',
        'id_field': 'id',
    },
    'OciCacheConfigSet': {
        'client': 'redis.OciCacheConfigSetClient',
        'method': 'delete_oci_cache_config_set',
        'id_field': 'id',
    },
    'OciCacheUser': {
        'client': 'redis.OciCacheUserClient',
        'method': 'delete_oci_cache_user',
        'id_field': 'id',
    },
    'OdaInstance': {
        'client': 'oda.OdaClient',
        'method': 'delete_oda_instance',
        'id_field': 'id',
    },
    'OdaPrivateEndpoint': {
        'client': 'oda.ManagementClient',
        'method': 'delete_oda_private_endpoint',
        'id_field': 'id',
    },
    'OdmsConnection': {
        'client': 'database_migration.DatabaseMigrationClient',
        'method': 'delete_connection',
        'id_field': 'id',
    },
    'OdmsJob': {
        'client': 'database_migration.DatabaseMigrationClient',
        'method': 'delete_job',
        'id_field': 'id',
    },
    'OdmsMigration': {
        'client': 'database_migration.DatabaseMigrationClient',
        'method': 'delete_migration',
        'id_field': 'id',
    },
    'OneoffPatch': {
        'client': 'database.DatabaseClient',
        'method': 'delete_oneoff_patch',
        'id_field': 'id',
    },
    'OnsSubscription': {
        'client': 'ons.NotificationDataPlaneClient',
        'method': 'delete_subscription',
        'id_field': 'id',
    },
    'OnsTopic': {
        'client': 'ons.NotificationControlPlaneClient',
        'method': 'delete_topic',
        'id_field': 'id',
    },
    'OpctlOperatorControl': {
        'client': 'operator_access_control.OperatorControlClient',
        'method': 'delete_operator_control',
        'id_field': 'id',
    },
    'OpctlOperatorControlAssignment': {
        'client': 'operator_access_control.OperatorControlAssignmentClient',
        'method': 'delete_operator_control_assignment',
        'id_field': 'id',
    },
    'OpensearchCluster': {
        'client': 'opensearch.OpensearchClusterClient',
        'method': 'delete_opensearch_cluster',
        'id_field': 'id',
    },
    'OpsiDatabaseInsight': {
        'client': 'opsi.OperationsInsightsClient',
        'method': 'delete_database_insight',
        'id_field': 'id',
    },
    'OracleDbAwsKey': {
        'client': 'dbmulticloud.DbMulticloudAwsProviderClient',
        'method': 'delete_oracle_db_aws_key',
        'id_field': 'id',
    },
    'OracleDbAzureConnector': {
        'client': 'dbmulticloud.OracleDBAzureConnectorClient',
        'method': 'delete_oracle_db_azure_connector',
        'id_field': 'id',
    },
    'OracleDbAzureVault': {
        'client': 'dbmulticloud.OracleDbAzureVaultClient',
        'method': 'delete_oracle_db_azure_vault',
        'id_field': 'id',
    },
    'OracleDbGcpIdentityConnector': {
        'client': 'dbmulticloud.DbMulticloudGCPProviderClient',
        'method': 'delete_oracle_db_gcp_identity_connector',
        'id_field': 'id',
    },
    'OrmConfigSourceProvider': {
        'client': 'resource_manager.ResourceManagerClient',
        'method': 'delete_configuration_source_provider',
        'id_field': 'id',
    },
    'OrmPrivateEndpoint': {
        'client': 'resource_manager.ResourceManagerClient',
        'method': 'delete_private_endpoint',
        'id_field': 'id',
    },
    'OrmStack': {
        'client': 'resource_manager.ResourceManagerClient',
        'method': 'delete_stack',
        'id_field': 'id',
    },
    'OrmTemplate': {
        'client': 'resource_manager.ResourceManagerClient',
        'method': 'delete_template',
        'id_field': 'id',
    },
    'OsmhLifecycleEnvironment': {
        'client': 'os_management_hub.LifecycleEnvironmentClient',
        'method': 'delete_lifecycle_environment',
        'id_field': 'id',
    },
    'OsmhManagementStation': {
        'client': 'os_management_hub.ManagementStationClient',
        'method': 'delete_management_station',
        'id_field': 'id',
    },
    'OsmhProfile': {
        'client': 'os_management_hub.OnboardingClient',
        'method': 'delete_profile',
        'id_field': 'id',
    },
    'OsmhScheduledJob': {
        'client': 'os_management_hub.ScheduledJobClient',
        'method': 'delete_scheduled_job',
        'id_field': 'id',
    },
    'OsmhSoftwareSource': {
        'client': 'os_management_hub.SoftwareSourceClient',
        'method': 'delete_software_source',
        'id_field': 'id',
    },
    'OutboundConnector': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_outbound_connector',
        'id_field': 'id',
    },
    'PingMonitor': {
        'client': 'healthchecks.HealthChecksClient',
        'method': 'delete_ping_monitor',
        'id_field': 'id',
    },
    'PluggableDatabase': {
        'client': 'database.DatabaseClient',
        'method': 'delete_pluggable_database',
        'id_field': 'id',
    },
    'Policy': {
        'client': 'identity.IdentityClient',
        'method': 'delete_policy',
        'id_field': 'id',
    },
    'PostgresqlBackup': {
        'client': 'psql.PostgresqlClient',
        'method': 'delete_backup',
        'id_field': 'id',
    },
    'PostgresqlDbSystem': {
        'client': 'psql.PostgresqlClient',
        'method': 'delete_db_system',
        'id_field': 'id',
    },
    'PreauthenticatedRequest': {
        'client': 'object_storage.ObjectStorageClient',
        'method': 'delete_preauthenticated_request',
        'id_field': 'id',
        'special': 'bucket',
    },
    'PrivateIp': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_private_ip',
        'id_field': 'id',
    },
    'ProcessAutomationInstance': {
        'client': 'opa.OpaInstanceClient',
        'method': 'delete_opa_instance',
        'id_field': 'id',
    },
    'ProtectedDatabase': {
        'client': 'recovery.DatabaseRecoveryClient',
        'method': 'delete_protected_database',
        'id_field': 'id',
    },
    'ProtectionPolicy': {
        'client': 'recovery.DatabaseRecoveryClient',
        'method': 'delete_protection_policy',
        'id_field': 'id',
    },
    'PublicIp': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_public_ip',
        'id_field': 'id',
    },
    'PublicIpPool': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_public_ip_pool',
        'id_field': 'id',
    },
    'Queue': {
        'client': 'queue.QueueAdminClient',
        'method': 'delete_queue',
        'id_field': 'id',
    },
    'Quota': {
        'client': 'limits.QuotasClient',
        'method': 'delete_quota',
        'id_field': 'id',
    },
    'RecoveryServiceSubnet': {
        'client': 'recovery.DatabaseRecoveryClient',
        'method': 'delete_recovery_service_subnet',
        'id_field': 'id',
    },
    'RedisCluster': {
        'client': 'redis.RedisClusterClient',
        'method': 'delete_redis_cluster',
        'id_field': 'id',
    },
    'RemotePeeringConnection': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_remote_peering_connection',
        'id_field': 'id',
    },
    'Replication': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_replication',
        'id_field': 'id',
    },
    'ReplicationSchedule': {
        'client': 'cloud_migrations.MigrationClient',
        'method': 'delete_replication_schedule',
        'id_field': 'id',
    },
    'ResourceSchedule': {
        'client': 'resource_scheduler.ScheduleClient',
        'method': 'delete_schedule',
        'id_field': 'id',
    },
    'RouteTable': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_route_table',
        'id_field': 'id',
    },
    'RoverCluster': {
        'client': 'rover.RoverClusterClient',
        'method': 'delete_rover_cluster',
        'id_field': 'id',
    },
    'RoverNode': {
        'client': 'rover.RoverNodeClient',
        'method': 'delete_rover_node',
        'id_field': 'id',
    },
    'SecurityAttributeNamespace': {
        'client': 'security_attribute.SecurityAttributeClient',
        'method': 'delete_security_attribute_namespace',
        'id_field': 'id',
    },
    'SecurityList': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_security_list',
        'id_field': 'id',
    },
    'SecurityZonesSecurityRecipe': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_security_recipe',
        'id_field': 'id',
    },
    'SecurityZonesSecurityZone': {
        'client': 'cloud_guard.CloudGuardClient',
        'method': 'delete_security_zone',
        'id_field': 'id',
    },
    'ServiceConnector': {
        'client': 'sch.ServiceConnectorClient',
        'method': 'delete_service_connector',
        'id_field': 'id',
    },
    'ServiceGateway': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_service_gateway',
        'id_field': 'id',
    },
    'Snapshot': {
        'client': 'file_storage.FileStorageClient',
        'method': 'delete_snapshot',
        'id_field': 'id',
    },
    'SteeringPolicy': {
        'client': 'dns.DnsClient',
        'method': 'delete_steering_policy',
        'id_field': 'id',
    },
    'SteeringPolicyAttachment': {
        'client': 'dns.DnsClient',
        'method': 'delete_steering_policy_attachment',
        'id_field': 'id',
    },
    'Stream': {
        'client': 'streaming.StreamAdminClient',
        'method': 'delete_stream',
        'id_field': 'id',
    },
    'StreamCdnConfig': {
        'client': 'media_services.MediaServicesClient',
        'method': 'delete_stream_cdn_config',
        'id_field': 'id',
    },
    'StreamDistributionChannel': {
        'client': 'media_services.MediaServicesClient',
        'method': 'delete_stream_distribution_channel',
        'id_field': 'id',
    },
    'StreamPackagingConfig': {
        'client': 'media_services.MediaServicesClient',
        'method': 'delete_stream_packaging_config',
        'id_field': 'id',
    },
    'StreamPool': {
        'client': 'streaming.StreamAdminClient',
        'method': 'delete_stream_pool',
        'id_field': 'id',
    },
    'Subnet': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_subnet',
        'id_field': 'id',
    },
    'TagDefault': {
        'client': 'identity.IdentityClient',
        'method': 'delete_tag_default',
        'id_field': 'id',
    },
    'TagNamespace': {
        'client': 'identity.IdentityClient',
        'method': 'delete_tag_namespace',
        'id_field': 'id',
    },
    'TsigKey': {
        'client': 'dns.DnsClient',
        'method': 'delete_tsig_key',
        'id_field': 'id',
    },
    'UnifiedAgentConfiguration': {
        'client': 'logging.LoggingManagementClient',
        'method': 'delete_unified_agent_configuration',
        'id_field': 'id',
    },
    'User': {
        'client': 'identity.IdentityClient',
        'method': 'delete_user',
        'id_field': 'id',
    },
    'Vault': {
        'client': 'key_management.KmsVaultClient',
        'method': 'schedule_vault_deletion',
        'id_field': 'id',
        'special': 'vault',
    },
    'VaultSecret': {
        'client': 'vault.VaultsClient',
        'method': 'schedule_secret_deletion',
        'id_field': 'id',
        'special': 'vault_secret',
    },
    'VbInstance': {
        'client': 'visual_builder.VbInstanceClient',
        'method': 'delete_vb_instance',
        'id_field': 'id',
    },
    'VbsInstance': {
        'client': 'vbs_inst.VbsInstanceClient',
        'method': 'delete_vbs_instance',
        'id_field': 'id',
    },
    'Vcn': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_vcn',
        'id_field': 'id',
        'dependencies': ['Subnet', 'InternetGateway', 'NatGateway', 'ServiceGateway', 'RouteTable', 'SecurityList', 'LocalPeeringGateway'],
    },
    'VirtualCircuit': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_virtual_circuit',
        'id_field': 'id',
    },
    'VisualBuilderInstance': {
        'client': 'visual_builder.VbInstanceClient',
        'method': 'delete_vb_instance',
        'id_field': 'id',
    },
    'Vlan': {
        'client': 'core.VirtualNetworkClient',
        'method': 'delete_vlan',
        'id_field': 'id',
    },
    'VmCluster': {
        'client': 'database.DatabaseClient',
        'method': 'delete_vm_cluster',
        'id_field': 'id',
    },
    'VmClusterNetwork': {
        'client': 'database.DatabaseClient',
        'method': 'delete_vm_cluster_network',
        'id_field': 'id',
    },
    'VmwareCluster': {
        'client': 'ocvp.ClusterClient',
        'method': 'delete_cluster',
        'id_field': 'id',
    },
    'VmwareEsxiHost': {
        'client': 'ocvp.EsxiHostClient',
        'method': 'delete_esxi_host',
        'id_field': 'id',
    },
    'VmwareSddc': {
        'client': 'ocvp.SddcClient',
        'method': 'delete_sddc',
        'id_field': 'id',
    },
    'Volume': {
        'client': 'core.BlockstorageClient',
        'method': 'delete_volume',
        'id_field': 'id',
        'composite': 'core.BlockstorageClientCompositeOperations',
        'composite_method': 'delete_volume_and_wait_for_state',
        'wait_states': ['TERMINATED'],
    },
    'VolumeAttachment': {
        'client': 'core.ComputeClient',
        'method': 'detach_volume',
        'id_field': 'id',
    },
    'VolumeBackup': {
        'client': 'core.BlockstorageClient',
        'method': 'delete_volume_backup',
        'id_field': 'id',
    },
    'VolumeBackupPolicy': {
        'client': 'core.BlockstorageClient',
        'method': 'delete_volume_backup_policy',
        'id_field': 'id',
    },
    'VolumeGroup': {
        'client': 'core.BlockstorageClient',
        'method': 'delete_volume_group',
        'id_field': 'id',
    },
    'VolumeGroupBackup': {
        'client': 'core.BlockstorageClient',
        'method': 'delete_volume_group_backup',
        'id_field': 'id',
    },
    'VssContainerScanRecipe': {
        'client': 'vulnerability_scanning.VulnerabilityScanningClient',
        'method': 'delete_container_scan_recipe',
        'id_field': 'id',
    },
    'VssContainerScanTarget': {
        'client': 'vulnerability_scanning.VulnerabilityScanningClient',
        'method': 'delete_container_scan_target',
        'id_field': 'id',
    },
    'VssHostScanRecipe': {
        'client': 'vulnerability_scanning.VulnerabilityScanningClient',
        'method': 'delete_host_scan_recipe',
        'id_field': 'id',
    },
    'VssHostScanTarget': {
        'client': 'vulnerability_scanning.VulnerabilityScanningClient',
        'method': 'delete_host_scan_target',
        'id_field': 'id',
    },
    'WaasAddressList': {
        'client': 'waas.WaasClient',
        'method': 'delete_address_list',
        'id_field': 'id',
    },
    'WaasCertificate': {
        'client': 'waas.WaasClient',
        'method': 'delete_certificate',
        'id_field': 'id',
    },
    'WaasCustomProtectionRule': {
        'client': 'waas.WaasClient',
        'method': 'delete_custom_protection_rule',
        'id_field': 'id',
    },
    'WaasPolicy': {
        'client': 'waas.WaasClient',
        'method': 'delete_waas_policy',
        'id_field': 'id',
    },
    'WebAppAcceleration': {
        'client': 'waa.WaaClient',
        'method': 'delete_web_app_acceleration',
        'id_field': 'id',
    },
    'WebAppAccelerationPolicy': {
        'client': 'waa.WaaClient',
        'method': 'delete_web_app_acceleration_policy',
        'id_field': 'id',
    },
    'WebAppFirewall': {
        'client': 'waf.WafClient',
        'method': 'delete_web_app_firewall',
        'id_field': 'id',
    },
    'WebAppFirewallNetworkAddressList': {
        'client': 'waf.WafClient',
        'method': 'delete_network_address_list',
        'id_field': 'id',
    },
    'WebAppFirewallPolicy': {
        'client': 'waf.WafClient',
        'method': 'delete_web_app_firewall_policy',
        'id_field': 'id',
    },
    'ZprPolicy': {
        'client': 'zpr.ZprClient',
        'method': 'delete_zpr_policy',
        'id_field': 'id',
    },
}
