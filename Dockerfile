# OCI Smart Delete - Web Application
#
# SECURITY: This image contains NO credentials
# Credentials are provided at runtime via:
#   - Volume mount: -v ~/.oci:/root/.oci:ro
#   - Environment variables: -e OCI_TENANCY_OCID=...
#   - Instance Principal: -e OCI_USE_INSTANCE_PRINCIPAL=true

# Multi-stage build for smaller final image
FROM python:3.14-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.14-slim

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /home/appuser/.oci && \
    chown -R appuser:appuser /home/appuser

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application files (NO CREDENTIALS!)
COPY web_app.py .
COPY oci_smart_delete.py .
COPY oci_resource_types.py .
COPY templates/ templates/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose Flask port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080', timeout=5)" || exit 1

# Runtime environment variables (no defaults with credentials!)
ENV PYTHONUNBUFFERED=1

# Run the application
# Credentials must be provided at runtime!
CMD ["python", "web_app.py"]
