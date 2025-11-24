#!/bin/bash

################################################################################
# OCI Smart Delete - Setup Script
#
# This script will:
# 1. Check Python installation
# 2. Install required dependencies
# 3. Verify OCI CLI configuration
# 4. Start the web application
################################################################################

set -e  # Exit on error

echo "================================================================================"
echo "OCI Smart Delete - Setup"
echo "================================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "ℹ $1"
}

# Step 1: Check Python installation
echo "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION is installed"
else
    print_error "Python 3 is not installed"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "  - macOS: brew install python3"
    echo "  - Linux: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo ""

# Step 2: Check pip installation
echo "Step 2: Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 is installed"
else
    print_error "pip3 is not installed"
    echo ""
    echo "Please install pip3:"
    echo "  - macOS: curl https://bootstrap.pypa.io/get-pip.py | python3"
    echo "  - Linux: sudo apt-get install python3-pip"
    exit 1
fi

echo ""

# Step 3: Set up virtual environment
echo "Step 3: Setting up Python virtual environment..."
echo ""

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Step 4: Installing Python dependencies..."
echo ""
print_info "Installing packages from requirements.txt..."

if pip install -r requirements.txt --quiet 2>&1 | grep -v "already satisfied"; then
    print_success "Dependencies installed successfully"
else
    print_success "All dependencies already installed"
fi

echo ""

# Step 5: Check for OCI CLI configuration
echo "Step 5: Checking OCI CLI configuration..."
echo ""
echo "IMPORTANT: OCI CLI credentials are REQUIRED for this application to work."
echo "If not found, you will need to set up OCI CLI before using this tool."
echo "Installation guide: https://docs.oracle.com/iaas/Content/API/SDKDocs/cliinstall.htm"
echo ""

OCI_CONFIG_FILE="$HOME/.oci/config"
OCI_CONFIG_FOUND=false

# Check default location
if [ -f "$OCI_CONFIG_FILE" ]; then
    print_success "Found OCI config at: $OCI_CONFIG_FILE"
    OCI_CONFIG_FOUND=true
else
    print_warning "OCI config not found at default location: $OCI_CONFIG_FILE"
fi

# If not found, ask user for custom location
if [ "$OCI_CONFIG_FOUND" = false ]; then
    echo ""
    echo "Do you have an OCI config file in a different location?"
    read -p "Enter the full path to your OCI config file (or press Enter to create one): " CUSTOM_CONFIG

    if [ -n "$CUSTOM_CONFIG" ] && [ -f "$CUSTOM_CONFIG" ]; then
        OCI_CONFIG_FILE="$CUSTOM_CONFIG"
        print_success "Using config file: $OCI_CONFIG_FILE"
        OCI_CONFIG_FOUND=true
    fi
fi

echo ""

# If still no config, provide instructions
if [ "$OCI_CONFIG_FOUND" = false ]; then
    echo ""
    echo "================================================================================"
    print_error "OCI CLI CREDENTIALS REQUIRED"
    echo "================================================================================"
    echo ""
    echo "This application requires OCI CLI credentials to access Oracle Cloud."
    echo "No credentials were found on your system."
    echo ""
    echo "================================================================================"
    echo "HOW TO SET UP OCI CLI CREDENTIALS:"
    echo "================================================================================"
    echo ""
    echo "Option 1: Install and Configure OCI CLI (RECOMMENDED)"
    echo ""
    echo "  Step 1: Install OCI CLI"
    echo "          macOS:  brew install oci-cli"
    echo "          Linux:  bash -c \"\$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)\""
    echo "          Installation guide: https://docs.oracle.com/iaas/Content/API/SDKDocs/cliinstall.htm"
    echo ""
    echo "  Step 2: Configure OCI CLI"
    echo "          Run: oci setup config"
    echo ""
    echo "  Step 3: Follow the prompts to enter:"
    echo "          - Your user OCID"
    echo "          - Your tenancy OCID"
    echo "          - Your home region"
    echo "          - Generate a new API key pair"
    echo ""
    echo "================================================================================"
    echo ""
    echo "Option 2: Manual API Key Setup (Advanced)"
    echo ""
    echo "  1. Login to Oracle Cloud Console: https://cloud.oracle.com"
    echo "  2. Click your profile icon → User Settings"
    echo "  3. Under 'Resources', click 'API Keys'"
    echo "  4. Click 'Add API Key' → 'Generate API Key Pair'"
    echo "  5. Download the private key file"
    echo "  6. Copy the configuration preview shown"
    echo "  7. Create directory: mkdir -p ~/.oci"
    echo "  8. Create file: ~/.oci/config"
    echo "  9. Paste the configuration into the config file"
    echo "  10. Save private key as: ~/.oci/oci_api_key.pem"
    echo "  11. Set permissions: chmod 600 ~/.oci/oci_api_key.pem"
    echo ""
    echo "================================================================================"
    echo ""
    echo "After setting up OCI CLI credentials, run this script again."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Step 6: Start the application
echo ""
echo "================================================================================"
echo "Starting OCI Smart Delete Web Interface"
echo "================================================================================"
echo ""
print_info "Starting the web server..."
echo ""
echo "Open your browser and navigate to:"
echo ""
echo "    http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================================================================"
echo ""

# Export config file path if custom
if [ "$OCI_CONFIG_FOUND" = true ] && [ "$OCI_CONFIG_FILE" != "$HOME/.oci/config" ]; then
    export OCI_CONFIG_FILE="$OCI_CONFIG_FILE"
fi

# Activate venv and start the application
source venv/bin/activate
python web_app.py
