#!/usr/bin/env python3
"""
OCI Resource Type Generator

This tool auto-discovers all OCI resource types and generates deletion mappings by:
1. Introspecting the OCI Python SDK for all clients and delete methods
2. Querying OCI Search service for all searchable resource types
3. Generating a comprehensive resource type mapping

Usage:
    python3 generate_resource_types.py [-cp <profile>] [-o <output_file>]
"""

import oci
import inspect
import argparse
import json
from collections import defaultdict
import re


class ResourceTypeGenerator:
    """Auto-discover OCI resource types from SDK"""

    def __init__(self, config, signer):
        self.config = config
        self.signer = signer
        self.resource_types = {}

    def scan_oci_sdk(self):
        """Scan the OCI SDK for all client classes and their delete methods"""
        print("Scanning OCI SDK for resource types...")

        # Common patterns for delete methods
        delete_patterns = [
            r'^delete_(.+)$',
            r'^terminate_(.+)$',
            r'^remove_(.+)$',
        ]

        # Track findings
        clients_found = []

        # Scan all modules in OCI SDK
        for module_name in dir(oci):
            if module_name.startswith('_'):
                continue

            try:
                module = getattr(oci, module_name)

                # Skip non-modules
                if not inspect.ismodule(module):
                    continue

                # Look for Client classes
                for class_name in dir(module):
                    if not class_name.endswith('Client'):
                        continue

                    if class_name.endswith('ClientCompositeOperations'):
                        continue

                    try:
                        client_class = getattr(module, class_name)

                        # Skip if not a class
                        if not inspect.isclass(client_class):
                            continue

                        client_path = f"{module_name}.{class_name}"
                        methods = []

                        # Find all delete/terminate methods
                        for method_name in dir(client_class):
                            if method_name.startswith('_'):
                                continue

                            # Check if it matches delete patterns
                            for pattern in delete_patterns:
                                match = re.match(pattern, method_name)
                                if match:
                                    resource_name = match.group(1)
                                    methods.append({
                                        'method': method_name,
                                        'resource': resource_name
                                    })

                        if methods:
                            clients_found.append({
                                'module': module_name,
                                'client': class_name,
                                'client_path': client_path,
                                'methods': methods
                            })

                    except Exception as e:
                        pass

            except Exception as e:
                pass

        print(f"Found {len(clients_found)} clients with delete methods")

        # Generate resource type mappings
        for client_info in clients_found:
            for method_info in client_info['methods']:
                # Convert snake_case to TitleCase for resource type
                resource_parts = method_info['resource'].split('_')
                resource_type = ''.join(word.capitalize() for word in resource_parts)

                # Check if there's a composite client
                composite_client = None
                composite_method = None

                composite_class_name = client_info['client'].replace('Client', 'ClientCompositeOperations')
                try:
                    module = getattr(oci, client_info['module'])
                    if hasattr(module, composite_class_name):
                        composite_client = f"{client_info['module']}.{composite_class_name}"
                        composite_method = f"{method_info['method']}_and_wait_for_state"
                except:
                    pass

                mapping = {
                    'client': client_info['client_path'],
                    'method': method_info['method'],
                    'id_field': 'id'
                }

                if composite_client:
                    mapping['composite'] = composite_client
                    mapping['composite_method'] = composite_method
                    mapping['wait_states'] = ['TERMINATED', 'DELETED']

                self.resource_types[resource_type] = mapping

        return clients_found

    def get_search_resource_types(self):
        """Query OCI Search service for all searchable resource types"""
        print("\nQuerying OCI Search service for resource types...")

        try:
            search_client = oci.resource_search.ResourceSearchClient(
                self.config, signer=self.signer
            )

            # Try to get all resource types by doing a broad search
            query = "query all resources"

            search_details = oci.resource_search.models.StructuredSearchDetails(
                query=query,
                type='Structured',
                matching_context_type='NONE'
            )

            resource_types_from_search = set()

            # Sample search to get various resource types
            try:
                response = search_client.search_resources(
                    search_details,
                    limit=1000
                )

                for item in response.data.items:
                    resource_types_from_search.add(item.resource_type)

            except Exception as e:
                print(f"  Warning: Could not query search service: {e}")

            print(f"Found {len(resource_types_from_search)} resource types from Search service")

            return sorted(resource_types_from_search)

        except Exception as e:
            print(f"  Error accessing Search service: {e}")
            return []

    def generate_python_code(self):
        """Generate Python code for the resource type map"""
        code = "# Auto-generated OCI Resource Type Mappings\n"
        code += "# Generated by generate_resource_types.py\n\n"
        code += "RESOURCE_TYPE_MAP = {\n"

        for resource_type in sorted(self.resource_types.keys()):
            mapping = self.resource_types[resource_type]
            code += f"    '{resource_type}': {{\n"
            code += f"        'client': '{mapping['client']}',\n"
            code += f"        'method': '{mapping['method']}',\n"
            code += f"        'id_field': '{mapping['id_field']}'\n"

            if 'composite' in mapping:
                code += f"        'composite': '{mapping['composite']}',\n"
                code += f"        'composite_method': '{mapping['composite_method']}',\n"
                code += f"        'wait_states': {mapping['wait_states']},\n"

            code += "    },\n"

        code += "}\n"

        return code

    def print_summary(self, clients_found, search_types):
        """Print a summary of findings"""
        print("\n" + "="*80)
        print("RESOURCE TYPE DISCOVERY SUMMARY")
        print("="*80)

        print(f"\nSDK Clients Found: {len(clients_found)}")
        print(f"Resource Types from SDK: {len(self.resource_types)}")
        print(f"Resource Types from Search: {len(search_types)}")

        print("\n--- Clients with Delete Methods ---")
        for client in sorted(clients_found, key=lambda x: x['client_path'])[:20]:
            print(f"\n{client['client_path']}")
            for method in client['methods'][:5]:
                print(f"  - {method['method']} ({method['resource']})")
            if len(client['methods']) > 5:
                print(f"  ... and {len(client['methods']) - 5} more")

        if len(clients_found) > 20:
            print(f"\n... and {len(clients_found) - 20} more clients")

        print("\n--- Sample Resource Types from Search ---")
        for rtype in sorted(search_types)[:30]:
            if rtype in self.resource_types:
                print(f"  ✓ {rtype} (mapped)")
            else:
                print(f"  ✗ {rtype} (NOT mapped - needs manual config)")

        if len(search_types) > 30:
            print(f"\n... and {len(search_types) - 30} more")

        # Find unmapped types
        unmapped = set(search_types) - set(self.resource_types.keys())
        if unmapped:
            print(f"\n--- Unmapped Resource Types ({len(unmapped)}) ---")
            print("These need manual configuration:")
            for rtype in sorted(unmapped)[:20]:
                print(f"  - {rtype}")
            if len(unmapped) > 20:
                print(f"  ... and {len(unmapped) - 20} more")


def main():
    parser = argparse.ArgumentParser(
        description='Auto-discover OCI resource types and generate deletion mappings'
    )
    parser.add_argument('-cp', '--config-profile', default='DEFAULT',
                       help='Config profile to use (default: DEFAULT)')
    parser.add_argument('-cf', '--config-file', default='~/.oci/config',
                       help='Config file path (default: ~/.oci/config)')
    parser.add_argument('-o', '--output', default='resource_type_mappings.py',
                       help='Output file for Python code (default: resource_type_mappings.py)')
    parser.add_argument('-j', '--json',
                       help='Also output as JSON file')

    args = parser.parse_args()

    # Load OCI config
    config = oci.config.from_file(args.config_file, args.config_profile)
    signer = oci.signer.Signer(
        tenancy=config['tenancy'],
        user=config['user'],
        fingerprint=config['fingerprint'],
        private_key_file_location=config['key_file'],
        pass_phrase=config.get('pass_phrase')
    )

    generator = ResourceTypeGenerator(config, signer)

    # Scan SDK
    clients_found = generator.scan_oci_sdk()

    # Get resource types from Search
    search_types = generator.get_search_resource_types()

    # Print summary
    generator.print_summary(clients_found, search_types)

    # Generate Python code
    python_code = generator.generate_python_code()

    # Save to file
    with open(args.output, 'w') as f:
        f.write(python_code)

    print(f"\n✓ Generated Python code: {args.output}")
    print(f"  Total resource types mapped: {len(generator.resource_types)}")

    # Save JSON if requested
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(generator.resource_types, f, indent=2)
        print(f"✓ Generated JSON: {args.json}")

    print("\n" + "="*80)
    print("Next Steps:")
    print("="*80)
    print("1. Review the generated mappings")
    print("2. Add special handling for unmapped types")
    print("3. Import into oci_smart_delete.py")
    print("4. Test with your compartment")


if __name__ == '__main__':
    main()
