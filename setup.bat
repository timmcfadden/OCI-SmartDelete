@echo off
REM ============================================================================
REM OCI Smart Delete - Setup Script (Windows)
REM
REM This script will:
REM 1. Check Python installation
REM 2. Install required dependencies
REM 3. Verify OCI CLI configuration
REM 4. Start the web application
REM ============================================================================

setlocal enabledelayedexpansion

echo ================================================================================
echo OCI Smart Delete - Setup
echo ================================================================================
echo.

REM Step 1: Check Python installation
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo SUCCESS: Python !PYTHON_VERSION! is installed
) else (
    echo ERROR: Python is not installed
    echo.
    echo Please install Python 3.7 or higher:
    echo   Download from: https://www.python.org/downloads/
    echo   Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo.

REM Step 2: Check pip installation
echo Step 2: Checking pip installation...
pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: pip is installed
) else (
    echo ERROR: pip is not installed
    echo.
    echo Please reinstall Python and ensure pip is included
    pause
    exit /b 1
)

echo.

REM Step 3: Install dependencies
echo Step 3: Installing Python dependencies...
echo.
echo Installing packages from requirements.txt...
echo This may take a minute...
echo.

pip install -r requirements.txt
if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: Dependencies installed successfully
) else (
    echo.
    echo WARNING: There was an issue installing dependencies
    echo You may need to run this script as Administrator
    echo.
    pause
)

echo.

REM Step 4: Check for OCI CLI configuration
echo Step 4: Checking OCI CLI configuration...
echo.
echo IMPORTANT: OCI CLI credentials are REQUIRED for this application to work.
echo If not found, you will need to set up OCI CLI before using this tool.
echo Installation guide: https://docs.oracle.com/iaas/Content/API/SDKDocs/cliinstall.htm
echo.

set OCI_CONFIG_FILE=%USERPROFILE%\.oci\config
set OCI_CONFIG_FOUND=false

REM Check default location
if exist "%OCI_CONFIG_FILE%" (
    echo SUCCESS: Found OCI config at: %OCI_CONFIG_FILE%
    set OCI_CONFIG_FOUND=true
) else (
    echo WARNING: OCI config not found at default location: %OCI_CONFIG_FILE%
)

REM If not found, ask user for custom location
if "!OCI_CONFIG_FOUND!"=="false" (
    echo.
    echo Do you have an OCI config file in a different location?
    set /p CUSTOM_CONFIG="Enter the full path to your OCI config file (or press Enter to skip): "

    if not "!CUSTOM_CONFIG!"=="" (
        if exist "!CUSTOM_CONFIG!" (
            set OCI_CONFIG_FILE=!CUSTOM_CONFIG!
            echo SUCCESS: Using config file: !OCI_CONFIG_FILE!
            set OCI_CONFIG_FOUND=true
        )
    )
)

echo.

REM If still no config, provide instructions
if "!OCI_CONFIG_FOUND!"=="false" (
    echo.
    echo ================================================================================
    echo ERROR: OCI CLI CREDENTIALS REQUIRED
    echo ================================================================================
    echo.
    echo This application requires OCI CLI credentials to access Oracle Cloud.
    echo No credentials were found on your system.
    echo.
    echo ================================================================================
    echo HOW TO SET UP OCI CLI CREDENTIALS:
    echo ================================================================================
    echo.
    echo Option 1: Install and Configure OCI CLI ^(RECOMMENDED^)
    echo.
    echo   Step 1: Install OCI CLI for Windows
    echo           Download from: https://docs.oracle.com/iaas/Content/API/SDKDocs/cliinstall.htm
    echo           Follow the Windows installation instructions
    echo.
    echo   Step 2: Configure OCI CLI
    echo           Open a new command prompt and run:
    echo           oci setup config
    echo.
    echo   Step 3: Follow the prompts to enter:
    echo           - Your user OCID
    echo           - Your tenancy OCID
    echo           - Your home region
    echo           - Generate a new API key pair
    echo.
    echo ================================================================================
    echo.
    echo Option 2: Manual API Key Setup ^(Advanced^)
    echo.
    echo   1. Login to Oracle Cloud Console: https://cloud.oracle.com
    echo   2. Click your profile icon -^> User Settings
    echo   3. Under 'Resources', click 'API Keys'
    echo   4. Click 'Add API Key' -^> 'Generate API Key Pair'
    echo   5. Download the private key file
    echo   6. Copy the configuration preview shown
    echo   7. Create directory: %USERPROFILE%\.oci
    echo   8. Create file: %USERPROFILE%\.oci\config
    echo   9. Paste the configuration into the config file
    echo   10. Save private key as: %USERPROFILE%\.oci\oci_api_key.pem
    echo.
    echo ================================================================================
    echo.
    echo After setting up OCI CLI credentials, run this script again.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Step 5: Start the application
echo.
echo ================================================================================
echo Starting OCI Smart Delete Web Interface
echo ================================================================================
echo.
echo Starting the web server...
echo.
echo Open your browser and navigate to:
echo.
echo     http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

REM Start the application
python web_app.py

REM If the application exits, pause so user can see any errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo.
    echo ERROR: The application exited with an error
    echo.
    pause
)
