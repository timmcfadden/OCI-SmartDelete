# Docker Deployment Guide

Complete guide for running OCI Smart Delete in Docker containers.

## 🔒 Security First

**✅ Your credentials are NEVER in the Docker image**
**✅ Credentials are only provided at runtime**
**✅ Multiple secure authentication methods supported**

---

## Quick Start

### Option 1: Using Pre-built Image (Fastest)

```bash
# Pull the latest image
docker pull ghcr.io/timmcfadden/oci-smartdelete:latest

# Run with your existing OCI credentials
docker run -v ~/.oci:/home/appuser/.oci:ro -p 8080:8080 \
  ghcr.io/timmcfadden/oci-smartdelete:latest

# Open http://localhost:8080
```

### Option 2: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/timmcfadden/OCI-SmartDelete.git
cd OCI-SmartDelete

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 3: Build Locally

```bash
# Build the image
docker build -t oci-smartdelete .

# Run it
docker run -v ~/.oci:/home/appuser/.oci:ro -p 8080:8080 oci-smartdelete
```

---

## Authentication Methods

### Method 1: Volume Mount (Best for Local Development)

**Mount your existing `~/.oci` directory:**

```bash
docker run -v ~/.oci:/home/appuser/.oci:ro -p 8080:8080 \
  ghcr.io/timmcfadden/oci-smartdelete:latest
```

**Advantages:**
- ✅ Uses existing OCI CLI configuration
- ✅ No credential copying
- ✅ Read-only mount (`:ro`) for security
- ✅ Works immediately if you have OCI CLI configured

**Requirements:**
- Must have `~/.oci/config` file
- Private key file referenced in config must exist

---

### Method 2: Environment Variables (Best for CI/CD)

**Step 1: Create `.env` file**

```bash
# Copy the template
cp .env.example .env

# Edit .env and fill in your credentials
# See .env.example for all options
```

**Step 2: Run with environment variables**

```bash
docker run --env-file .env -p 8080:8080 \
  ghcr.io/timmcfadden/oci-smartdelete:latest
```

**Or pass variables directly:**

```bash
docker run \
  -e OCI_TENANCY_OCID="ocid1.tenancy.oc1..aaa..." \
  -e OCI_USER_OCID="ocid1.user.oc1..aaa..." \
  -e OCI_FINGERPRINT="aa:bb:cc:..." \
  -e OCI_REGION="us-ashburn-1" \
  -e OCI_PRIVATE_KEY="$(cat ~/.oci/oci_api_key.pem | awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}')" \
  -p 8080:8080 \
  ghcr.io/timmcfadden/oci-smartdelete:latest
```

**Advantages:**
- ✅ No file mounting required
- ✅ Perfect for cloud deployments
- ✅ Easy to integrate with secret managers
- ✅ Works in CI/CD pipelines

**Requirements:**
- Set environment variables: `OCI_TENANCY_OCID`, `OCI_USER_OCID`, `OCI_FINGERPRINT`, `OCI_REGION`, `OCI_PRIVATE_KEY`

---

### Method 3: Instance Principal (Best for OCI Deployments)

**When running in OCI (Container Instances, Compute):**

```bash
docker run \
  -e OCI_USE_INSTANCE_PRINCIPAL=true \
  -p 8080:8080 \
  ghcr.io/timmcfadden/oci-smartdelete:latest
```

**Advantages:**
- ✅ **ZERO credentials needed!**
- ✅ Most secure method
- ✅ Credentials managed by OCI IAM
- ✅ No key files or environment variables

**Requirements:**
- Must be running on OCI infrastructure (Container Instances, Compute Instance)
- Instance/Container must have appropriate IAM policies

---

## Docker Compose Configuration

### Basic Configuration

**docker-compose.yml** (included in repository):

```yaml
version: '3.8'

services:
  oci-smart-delete:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    ports:
      - "8080:8080"
    volumes:
      - ~/.oci:/home/appuser/.oci:ro
    restart: unless-stopped
```

### Using Environment Variables

```yaml
version: '3.8'

services:
  oci-smart-delete:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    ports:
      - "8080:8080"
    env_file:
      - .env  # Create from .env.example
    restart: unless-stopped
```

### Custom Port

```yaml
version: '3.8'

services:
  oci-smart-delete:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    ports:
      - "9000:8080"  # Access at http://localhost:9000
    volumes:
      - ~/.oci:/home/appuser/.oci:ro
```

---

## Building the Image

### Standard Build

```bash
docker build -t oci-smartdelete:latest .
```

### Multi-Platform Build

```bash
# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 \
  -t oci-smartdelete:latest .
```

### Build with Custom Tag

```bash
docker build -t oci-smartdelete:v1.0.0 .
```

---

## Security Best Practices

### 1. Use Read-Only Volume Mounts

```bash
# Always use :ro (read-only) when mounting credentials
docker run -v ~/.oci:/home/appuser/.oci:ro ...
```

### 2. Limit Environment Variable Exposure

```bash
# Use .env file instead of command-line arguments
# Command-line args are visible in `docker ps` and logs
docker run --env-file .env ...  # ✅ Good

# Avoid this:
docker run -e OCI_PRIVATE_KEY="-----BEGIN..." ...  # ❌ Visible in process list
```

### 3. Use Docker Secrets (Production)

```yaml
version: '3.8'

services:
  oci-smart-delete:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    secrets:
      - oci_private_key
    environment:
      - OCI_TENANCY_OCID=${OCI_TENANCY_OCID}
      - OCI_USER_OCID=${OCI_USER_OCID}
      - OCI_FINGERPRINT=${OCI_FINGERPRINT}
      - OCI_REGION=${OCI_REGION}
      - OCI_PRIVATE_KEY_FILE=/run/secrets/oci_private_key

secrets:
  oci_private_key:
    file: ~/.oci/oci_api_key.pem
```

### 4. Verify Image Has No Credentials

```bash
# Inspect the image
docker run ghcr.io/timmcfadden/oci-smartdelete:latest find / -name "*.pem" 2>/dev/null
# Should return nothing

# Check for environment variables in image
docker inspect ghcr.io/timmcfadden/oci-smartdelete:latest | grep -i oci
# Should not show any credentials
```

### 5. Set Proper File Permissions

```bash
# Ensure your credential files have restricted permissions
chmod 600 ~/.oci/config
chmod 600 ~/.oci/oci_api_key.pem
chmod 700 ~/.oci
```

---

## Troubleshooting

### "Config file not found"

**Problem:** Container can't find `~/.oci/config`

**Solution:**
```bash
# Check if file exists on your machine
ls -la ~/.oci/config

# If using volume mount, ensure path is correct
docker run -v ~/.oci:/home/appuser/.oci:ro ...

# Or use environment variables instead
docker run --env-file .env ...
```

### "Permission denied" when reading credentials

**Problem:** Container can't read mounted files

**Solution:**
```bash
# Fix permissions on your machine
chmod 600 ~/.oci/config
chmod 600 ~/.oci/oci_api_key.pem

# Ensure files are owned by you
ls -la ~/.oci/
```

### "Invalid private key format"

**Problem:** Environment variable private key format is wrong

**Solution:**
```bash
# Convert PEM to single-line with escaped newlines
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' ~/.oci/oci_api_key.pem

# Or use base64 encoding
cat ~/.oci/oci_api_key.pem | base64 -w0
# Then set OCI_PRIVATE_KEY_BASE64 instead of OCI_PRIVATE_KEY
```

### Port already in use

**Problem:** Port 8080 is already used by another application

**Solution:**
```bash
# Use a different port
docker run -v ~/.oci:/home/appuser/.oci:ro -p 8081:8080 ...

# Or stop the conflicting container
docker ps  # Find the container
docker stop <container-id>
```

### Container exits immediately

**Problem:** Application crashes on startup

**Solution:**
```bash
# Check logs
docker logs <container-id>

# Common issues:
# - No authentication method configured
# - Invalid credentials
# - Missing required environment variables

# Test authentication:
docker run -it --entrypoint /bin/bash ghcr.io/timmcfadden/oci-smartdelete:latest
# Then manually test: python web_app.py
```

---

## Advanced Usage

### Running Multiple Instances

```yaml
version: '3.8'

services:
  oci-smart-delete-dev:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    ports:
      - "8080:8080"
    env_file:
      - .env.dev

  oci-smart-delete-prod:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    ports:
      - "8081:8080"
    env_file:
      - .env.prod
```

### With Reverse Proxy (Nginx)

```yaml
version: '3.8'

services:
  oci-smart-delete:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    volumes:
      - ~/.oci:/home/appuser/.oci:ro
    # Don't expose port directly

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - oci-smart-delete
```

### Resource Limits

```yaml
version: '3.8'

services:
  oci-smart-delete:
    image: ghcr.io/timmcfadden/oci-smartdelete:latest
    volumes:
      - ~/.oci:/home/appuser/.oci:ro
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## Deployment Examples

### Local Development

```bash
# Quick start with existing credentials
docker-compose up -d

# View logs
docker-compose logs -f

# Access at http://localhost:8080
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
- name: Run OCI Smart Delete
  run: |
    docker run -d \
      -e OCI_TENANCY_OCID=${{ secrets.OCI_TENANCY_OCID }} \
      -e OCI_USER_OCID=${{ secrets.OCI_USER_OCID }} \
      -e OCI_FINGERPRINT=${{ secrets.OCI_FINGERPRINT }} \
      -e OCI_REGION=${{ secrets.OCI_REGION }} \
      -e OCI_PRIVATE_KEY=${{ secrets.OCI_PRIVATE_KEY }} \
      -p 8080:8080 \
      ghcr.io/timmcfadden/oci-smartdelete:latest
```

### OCI Container Instances

```bash
# Deploy to OCI Container Instances with Instance Principal
oci container-instances container-instance create \
  --compartment-id ocid1.compartment.oc1..aaa... \
  --availability-domain AD-1 \
  --shape CI.Standard.E4.Flex \
  --containers '[{
    "imageUrl": "ghcr.io/timmcfadden/oci-smartdelete:latest",
    "environmentVariables": {
      "OCI_USE_INSTANCE_PRINCIPAL": "true"
    }
  }]'
```

---

## Image Tags

| Tag | Description | Use Case |
|-----|-------------|----------|
| `latest` | Latest stable release | Production |
| `v1.0.0` | Specific version | Version pinning |
| `nightly` | Development build | Testing new features |

```bash
# Use specific version
docker pull ghcr.io/timmcfadden/oci-smartdelete:v1.0.0

# Use latest (recommended)
docker pull ghcr.io/timmcfadden/oci-smartdelete:latest
```

---

## Health Checks

The container includes a built-in health check:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' <container-id>

# View health check logs
docker inspect --format='{{json .State.Health}}' <container-id> | jq
```

---

## Next Steps

- [Authentication Setup Guide](.env.example) - Detailed credential configuration
- [OCI Container Instances Deployment](README.md#oci-deployment) - One-click OCI deployment
- [Kubernetes Deployment](kubernetes/) - Production-grade deployments

---

## Support

- [GitHub Issues](https://github.com/timmcfadden/OCI-SmartDelete/issues)
- [GitHub Discussions](https://github.com/timmcfadden/OCI-SmartDelete/discussions)

---

**Remember: Your credentials stay safe! They're never in the image, only provided at runtime.**
