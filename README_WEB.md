# OCI Smart Delete - Web Interface 🌐

A beautiful web-based interface for OCI Smart Delete, built with Flask, Alpine.js, and Tailwind CSS.

## Features ✨

- **Visual Compartment Selection** - Browse and select compartments from a dropdown
- **Real-time Resource Discovery** - See exactly what's in your compartment in seconds
- **Beautiful UI** - Modern, responsive design with Tailwind CSS
- **Interactive** - Expand resource details, see counts, and track progress
- **Safe Deletion** - Clear warnings and confirmations before deletion
- **Optional Compartment Deletion** - Choose to delete just resources or the compartment too
- **Live Results** - See deletion progress and results in real-time

## Quick Start 🚀

### Super Easy Setup (Recommended)

**Mac/Linux:**
```bash
git clone https://github.com/yourusername/OCI-SmartDelete.git
cd OCI-SmartDelete
./setup.sh
```

**Windows:**
```cmd
git clone https://github.com/yourusername/OCI-SmartDelete.git
cd OCI-SmartDelete
setup.bat
```

The setup script will:
- ✅ Check Python installation
- ✅ Install dependencies
- ✅ Verify OCI credentials
- ✅ Start the web server

Then open: **http://localhost:8080**

### Manual Setup

**1. Install Dependencies**

```bash
pip3 install -r requirements.txt
```

**2. Configure OCI Credentials** (if not already done)

```bash
# Option 1: Use OCI CLI
oci setup config

# Option 2: Manual - create ~/.oci/config
# See "OCI Credentials" section below
```

**3. Start the Web Server**

```bash
python3 web_app.py
```

**4. Open Your Browser**

Navigate to: **http://localhost:8080**

## How to Use 📖

### Step 1: Select Compartment
1. The page loads and automatically fetches all compartments
2. Select a compartment from the dropdown
3. Click "Refresh" to reload compartments if needed

### Step 2: Discover Resources
1. Click "🔍 Discover Resources"
2. See instant results:
   - Total resources count
   - Number of resource types
   - Discovery time (usually <1 second!)
3. Expand resource types to see details

### Step 3: Delete
1. **Option 1**: Delete resources only (keeps compartment)
2. **Option 2**: Check "Also delete the compartment" for full cleanup
3. Click the delete button
4. Confirm the action
5. Watch real-time deletion progress
6. Review results

## Screenshots 📸

### Main Interface
```
┌─────────────────────────────────────────────────┐
│  OCI Smart Delete                               │
│  Fast compartment cleanup                       │
├─────────────────────────────────────────────────┤
│  ① Select Compartment                           │
│  ┌───────────────────────────┐                  │
│  │ Choose a compartment...   ▼│                 │
│  └───────────────────────────┘  [🔄 Refresh]    │
├─────────────────────────────────────────────────┤
│  ② Discover Resources                           │
│                    [🔍 Discover Resources]       │
│                                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │   25    │ │    8    │ │  0.4s   │          │
│  │Resources│ │  Types  │ │  Time   │          │
│  └─────────┘ └─────────┘ └─────────┘          │
│                                                  │
│  📦 Instance (5 resources)     [Show Details ▼] │
│  📦 Volume (10 resources)      [Show Details ▼] │
│  📦 LoadBalancer (2 resources) [Show Details ▼] │
├─────────────────────────────────────────────────┤
│  ③ Delete Resources                             │
│  ⚠️  Deletion Options                           │
│  ☐ Also delete the compartment                  │
│                                                  │
│  [🗑️ Delete Resources Only]                    │
└─────────────────────────────────────────────────┘
```

## API Endpoints 🔌

### GET `/api/compartments`
Returns list of all compartments in the tenancy.

**Response:**
```json
{
  "compartments": [
    {
      "id": "ocid1.compartment...",
      "name": "Production",
      "description": "Production environment",
      "state": "ACTIVE",
      "is_root": false
    }
  ],
  "tenancy_name": "MyTenancy"
}
```

### POST `/api/discover`
Discovers resources in a compartment.

**Request:**
```json
{
  "compartment_id": "ocid1.compartment..."
}
```

**Response:**
```json
{
  "resources": [
    {
      "type": "Instance",
      "count": 5,
      "items": [...]
    }
  ],
  "total_count": 25,
  "type_count": 8
}
```

### POST `/api/delete`
Deletes resources from a compartment.

**Request:**
```json
{
  "compartment_id": "ocid1.compartment...",
  "delete_compartment": false
}
```

**Response:**
```json
{
  "success": true,
  "deleted_count": 25,
  "failed_count": 0,
  "deleted_by_type": {...},
  "failed_by_type": {...},
  "logs": "..."
}
```

## Technology Stack 💻

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Flask | REST API server |
| **Frontend Framework** | Alpine.js | Reactive UI components |
| **Styling** | Tailwind CSS | Beautiful, responsive design |
| **OCI SDK** | Python OCI SDK | Cloud API interactions |
| **Core Logic** | oci_smart_delete.py | Resource deletion engine |

## Features in Detail

### Real-time Discovery
- Uses OCI Search service for instant results
- Shows resource counts by type
- Expandable details for each resource
- Displays resource state and region

### Smart Deletion
- Processes resources in dependency order
- Auto-retry for failed deletions
- Parallel processing for speed
- Detailed progress logging

### Safety Features
- Confirmation dialogs before deletion
- Clear visual warnings
- Different colors for resource-only vs full deletion
- Real-time result tracking

### Responsive Design
- Works on desktop, tablet, and mobile
- Clean, modern interface
- Loading states and spinners
- Color-coded status indicators

## OCI Credentials Setup 🔑

The web app uses your OCI CLI configuration file (usually `~/.oci/config`).

### Option 1: OCI CLI (Easiest)
```bash
# Install OCI CLI (if not installed)
# Mac: brew install oci-cli
# Windows: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm

# Configure credentials
oci setup config
```

### Option 2: Manual Setup
1. Go to [cloud.oracle.com](https://cloud.oracle.com) and login
2. Click Profile → User Settings
3. Under "Resources" → API Keys → Add API Key
4. Generate API Key Pair → Download private key
5. Copy the configuration and create `~/.oci/config`:

**Mac/Linux** (`~/.oci/config`):
```ini
[DEFAULT]
user=ocid1.user.oc1..aaaa...
fingerprint=xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx
tenancy=ocid1.tenancy.oc1..aaaa...
region=us-ashburn-1
key_file=~/.oci/oci_api_key.pem
```

**Windows** (`%USERPROFILE%\.oci\config`):
```ini
[DEFAULT]
user=ocid1.user.oc1..aaaa...
fingerprint=xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx
tenancy=ocid1.tenancy.oc1..aaaa...
region=us-ashburn-1
key_file=C:\Users\YourName\.oci\oci_api_key.pem
```

6. Save your private key to the `key_file` location

### Option 3: Web Form (No File Setup)
If you don't have a config file, use the web interface:
- Go to `http://localhost:8080/login`
- Enter credentials directly in the form

## Configuration ⚙️

### Custom Config File Location
```bash
export OCI_CONFIG_FILE=/path/to/your/config
python3 web_app.py
```

### Use Different Profile
The app uses `[DEFAULT]` profile. To use a different one, you can modify session settings or edit the code:

```python
session['config_profile'] = 'PRODUCTION'
session['config_file'] = '/path/to/config'
```

## Development 🔧

### Run in Debug Mode
```bash
python3 web_app.py
# Server runs with auto-reload enabled
```

### Change Port
Edit `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 8080
```

### Add Custom Styling
Edit `templates/index.html` and modify Tailwind classes or add custom CSS.

## Security Notes 🔒

⚠️ **Important Security Considerations:**

1. **Development Server**: The included Flask server is for development only
   - For production, use a proper WSGI server (Gunicorn, uWSGI)

2. **Authentication**: No built-in authentication
   - Add your own auth layer for production use
   - Restrict network access appropriately

3. **OCI Credentials**: Uses local OCI config file
   - Ensure proper file permissions (chmod 600)
   - Never expose credentials in the web interface

4. **Network Exposure**: Default binds to 0.0.0.0
   - Change to 127.0.0.1 for local-only access
   - Use firewall rules in production

## Troubleshooting 🔍

### Port Already in Use
```bash
# Use a different port
# Edit web_app.py and change port=8080 to port=8081
```

### OCI Config Not Found
```bash
# Check your OCI config file exists
ls ~/.oci/config

# Or specify a different location in the code
```

### Permission Errors
```bash
# Ensure OCI config has correct permissions
chmod 600 ~/.oci/config
```

### Resources Not Showing
- Check compartment has resources
- Verify OCI credentials have read permissions
- Check browser console for errors

## Comparison: CLI vs Web

| Feature | CLI Tool | Web Interface |
|---------|----------|---------------|
| **Speed** | ⚡ Fastest | Fast |
| **Ease of Use** | Tech-savvy users | Everyone |
| **Visualization** | Text output | Beautiful UI |
| **Discovery** | Command required | Click button |
| **Resource Details** | Full logs | Expandable cards |
| **Best For** | Automation, scripts | Interactive use |

## Future Enhancements 🚀

Potential improvements:
- [ ] Multi-compartment batch deletion
- [ ] Schedule deletions
- [ ] User authentication
- [ ] Deletion history/audit log
- [ ] Resource type filtering
- [ ] Export results to CSV/JSON
- [ ] Dark mode toggle
- [ ] Progress bar for long deletions

## Support

For issues or questions:
- Check the main README.md
- Review the troubleshooting section
- Open an issue on GitHub

## License

Same as parent project (OCI-SuperDelete)

---

**Enjoy the beautiful web interface for OCI Smart Delete!** 🎉
