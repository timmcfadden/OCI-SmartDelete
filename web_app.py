#!/usr/bin/env python3
"""
OCI Smart Delete - Web Interface

A Flask-based web application for managing OCI compartment cleanup
with a beautiful UI using Alpine.js and Tailwind CSS
"""

from flask import Flask, render_template, request, jsonify, session
import oci
import logging
from oci_smart_delete import OCISmartDelete
import os
import secrets
from functools import wraps
import threading
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global dictionary to track active deletion jobs
deletion_jobs = {}  # {compartment_id: deleter_instance}


def get_oci_config():
    """
    Load OCI configuration with multiple authentication methods.

    Priority order:
    1. Instance Principal (OCI_USE_INSTANCE_PRINCIPAL=true)
    2. Environment Variables (OCI_TENANCY_OCID, etc.)
    3. Config File (~/.oci/config or OCI_CONFIG_FILE)

    Returns:
        tuple: (config dict, signer object) or (None, None) on failure
    """

    # =========================================================================
    # Method 1: Instance Principal (Best for OCI deployments)
    # =========================================================================
    if os.getenv('OCI_USE_INSTANCE_PRINCIPAL', '').lower() == 'true':
        logger.info("Using OCI Instance Principal authentication")
        try:
            signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
            # Build minimal config for Instance Principal
            config = {
                'region': os.getenv('OCI_REGION', 'us-ashburn-1'),
                'tenancy': signer.tenancy_id
            }
            logger.info(f"Instance Principal authentication successful for tenancy: {signer.tenancy_id}")
            return config, signer
        except Exception as e:
            logger.error(f"Instance Principal authentication failed: {e}")
            logger.info("Falling back to environment variables or config file...")

    # =========================================================================
    # Method 2: Environment Variables (Best for Docker/CI/CD)
    # =========================================================================
    required_env_vars = ['OCI_TENANCY_OCID', 'OCI_USER_OCID', 'OCI_FINGERPRINT', 'OCI_REGION']
    if all(os.getenv(var) for var in required_env_vars):
        logger.info("Using environment variables for authentication")
        try:
            # Get private key from environment
            private_key_env = os.getenv('OCI_PRIVATE_KEY')
            private_key_base64 = os.getenv('OCI_PRIVATE_KEY_BASE64')

            if not private_key_env and not private_key_base64:
                logger.error("OCI_PRIVATE_KEY or OCI_PRIVATE_KEY_BASE64 must be set")
                raise ValueError("Private key not found in environment variables")

            # Handle base64-encoded key if provided
            if private_key_base64:
                import base64
                private_key_content = base64.b64decode(private_key_base64).decode('utf-8')
                logger.info("Using base64-encoded private key")
            else:
                # Convert escaped newlines to actual newlines
                private_key_content = private_key_env.replace('\\n', '\n')
                logger.info("Using escaped newline private key")

            # Build config dictionary
            config = {
                'user': os.getenv('OCI_USER_OCID'),
                'tenancy': os.getenv('OCI_TENANCY_OCID'),
                'fingerprint': os.getenv('OCI_FINGERPRINT'),
                'region': os.getenv('OCI_REGION'),
                'key_content': private_key_content
            }

            # Add passphrase if provided
            passphrase = os.getenv('OCI_PASSPHRASE')
            if passphrase:
                config['pass_phrase'] = passphrase

            # Validate config
            oci.config.validate_config(config)

            # Create signer
            signer = oci.signer.Signer(
                tenancy=config['tenancy'],
                user=config['user'],
                fingerprint=config['fingerprint'],
                private_key_content=config['key_content'],
                pass_phrase=config.get('pass_phrase')
            )

            logger.info(f"Environment variable authentication successful for tenancy: {config['tenancy']}")
            return config, signer

        except Exception as e:
            logger.error(f"Environment variable authentication failed: {e}")
            logger.info("Falling back to config file...")

    # =========================================================================
    # Method 3: Config File (Traditional method)
    # =========================================================================
    logger.info("Using config file for authentication")
    profile = 'DEFAULT'
    config_file = os.path.expanduser('~/.oci/config')

    # Check for environment variable override
    if 'OCI_CONFIG_FILE' in os.environ:
        config_file = os.environ['OCI_CONFIG_FILE']
        logger.info(f"Using config file from OCI_CONFIG_FILE: {config_file}")
    else:
        logger.info(f"Using default config file: {config_file}")

    try:
        config = oci.config.from_file(config_file, profile)

        # Check if using session token from file (for oci session authenticate)
        if 'security_token_file' in config:
            token_file = os.path.expanduser(config['security_token_file'])
            with open(token_file, 'r') as f:
                token = f.read()
            private_key = oci.signer.load_private_key_from_file(config['key_file'])
            signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
            logger.info("Using session token authentication from config file")
        else:
            # Standard API key auth
            signer = oci.signer.Signer(
                tenancy=config['tenancy'],
                user=config['user'],
                fingerprint=config['fingerprint'],
                private_key_file_location=config['key_file'],
                pass_phrase=config.get('pass_phrase')
            )
            logger.info("Using API key authentication from config file")

        logger.info(f"Config file authentication successful for tenancy: {config['tenancy']}")
        return config, signer

    except FileNotFoundError:
        logger.error(f"Config file not found: {config_file}")
        logger.error("No authentication method available!")
        logger.error("Please provide credentials via:")
        logger.error("  1. Instance Principal (set OCI_USE_INSTANCE_PRINCIPAL=true)")
        logger.error("  2. Environment variables (set OCI_TENANCY_OCID, OCI_USER_OCID, etc.)")
        logger.error("  3. Config file (create ~/.oci/config)")
        return None, None
    except Exception as e:
        logger.error(f"Error loading OCI config from file: {e}")
        return None, None


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/compartments', methods=['GET'])
def list_compartments():
    """List all compartments in the tenancy"""
    try:
        config, signer = get_oci_config()
        if not config:
            return jsonify({'error': 'OCI configuration not found'}), 500

        identity = oci.identity.IdentityClient(config, signer=signer)

        # Get tenancy info
        tenancy = identity.get_tenancy(config['tenancy']).data

        # List all compartments (including sub-compartments)
        compartments = []

        # Add root compartment
        compartments.append({
            'id': config['tenancy'],
            'name': tenancy.name + ' (root)',
            'description': tenancy.description or '',
            'state': 'ACTIVE',
            'is_root': True
        })

        # Get all compartments
        def get_compartments_recursive(parent_id, level=0):
            try:
                response = identity.list_compartments(
                    parent_id,
                    compartment_id_in_subtree=True
                )

                for comp in response.data:
                    if comp.lifecycle_state in ['ACTIVE', 'DELETING']:
                        indent = '  ' * level
                        compartments.append({
                            'id': comp.id,
                            'name': f"{indent}{comp.name}",
                            'description': comp.description or '',
                            'state': comp.lifecycle_state,
                            'is_root': False,
                            'level': level
                        })
            except Exception as e:
                logger.error(f"Error listing compartments for {parent_id}: {e}")

        get_compartments_recursive(config['tenancy'])

        return jsonify({
            'compartments': compartments,
            'tenancy_name': tenancy.name
        })

    except Exception as e:
        logger.error(f"Error listing compartments: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/discover', methods=['POST'])
def discover_resources():
    """Discover resources in a compartment"""
    try:
        data = request.json
        compartment_id = data.get('compartment_id')

        if not compartment_id:
            return jsonify({'error': 'compartment_id is required'}), 400

        config, signer = get_oci_config()
        if not config:
            return jsonify({'error': 'OCI configuration not found'}), 500

        # Create deleter instance
        deleter = OCISmartDelete(
            config=config,
            signer=signer,
            compartment_id=compartment_id,
            force=True
        )

        # Discover resources
        resources_by_type = deleter.discover_resources()

        # Format for frontend
        resources = []
        total_count = 0

        for resource_type, items in resources_by_type.items():
            total_count += len(items)
            resources.append({
                'type': resource_type,
                'count': len(items),
                'items': [
                    {
                        'id': item.identifier,
                        'name': getattr(item, 'display_name', item.identifier),
                        'state': getattr(item, 'lifecycle_state', 'UNKNOWN'),
                        'region': getattr(item, 'region', 'unknown')
                    }
                    for item in items[:10]  # Limit to first 10 for display
                ]
            })

        return jsonify({
            'resources': resources,
            'total_count': total_count,
            'type_count': len(resources_by_type)
        })

    except Exception as e:
        logger.error(f"Error discovering resources: {e}")
        return jsonify({'error': str(e)}), 500


def run_deletion_background(deleter):
    """Background thread function to run deletion"""
    try:
        deleter.delete_all()
    except Exception as e:
        logger.error(f"Error in background deletion: {e}")
        deleter.progress['status'] = 'error'
        deleter.progress['phase'] = f'Error: {str(e)}'


@app.route('/api/delete', methods=['POST'])
def delete_resources():
    """Start deletion process in background"""
    try:
        data = request.json
        compartment_id = data.get('compartment_id')
        delete_compartment = data.get('delete_compartment', False)

        if not compartment_id:
            return jsonify({'error': 'compartment_id is required'}), 400

        config, signer = get_oci_config()
        if not config:
            return jsonify({'error': 'OCI configuration not found'}), 500

        # Create deleter instance
        deleter = OCISmartDelete(
            config=config,
            signer=signer,
            compartment_id=compartment_id,
            force=True,
            delete_compartment=delete_compartment
        )

        # Store deleter instance for progress tracking
        deletion_jobs[compartment_id] = deleter

        # Run deletion in background thread
        thread = threading.Thread(target=run_deletion_background, args=(deleter,))
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'message': 'Deletion started',
            'compartment_id': compartment_id
        })

    except Exception as e:
        logger.error(f"Error starting deletion: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete/progress/<compartment_id>', methods=['GET'])
def get_deletion_progress(compartment_id):
    """Get deletion progress for a compartment"""
    if compartment_id not in deletion_jobs:
        return jsonify({'error': 'No deletion job found'}), 404

    deleter = deletion_jobs[compartment_id]

    # Build response with current progress
    progress = deleter.progress.copy()

    # Remove non-serializable fields
    if 'processed_ids' in progress:
        del progress['processed_ids']

    # Convert resources_status dict to list for easier frontend consumption
    resources_list = []
    for res_id, res_info in progress['resources_status'].items():
        resources_list.append({
            'id': res_id,
            **res_info
        })

    progress['resources'] = resources_list
    del progress['resources_status']  # Remove dict version

    # Add summary counts
    progress['deleted_count'] = sum(deleter.deleted_count.values())
    progress['failed_count'] = sum(deleter.failed_count.values())
    progress['scheduled_count'] = sum(deleter.scheduled_count.values())
    progress['retriable_count'] = sum(deleter.retriable_count.values())

    return jsonify(progress)


if __name__ == '__main__':
    print("="*80)
    print("OCI Smart Delete - Web Interface")
    print("="*80)
    print("\nStarting web server...")
    print("Open your browser and navigate to: http://localhost:8080")
    print("\nPress Ctrl+C to stop the server")
    print("\nNOTE: Server is only accessible from this machine (localhost)")
    print("="*80)

    app.run(debug=True, host='127.0.0.1', port=8080)
