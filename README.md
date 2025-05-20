# Network Looking Glass

A modern, extensible web interface for real-time network troubleshooting.

Network Looking Glass is a Flask-based web application that provides a "looking glass" interface for interacting with network routers via SSH. It allows users to fetch available routers for a given ASN and execute both standard and custom commands on them through a web interface.

## Features

- List routers by ASN
- Execute standard commands (BGP, ping, traceroute) on routers via SSH
- **Custom Command Support:** Enter and execute any router command via the GUI
- Stream command output to the browser in real time
- UI dynamically hides/shows relevant input fields based on command type
- Simple REST API endpoints

## Requirements

- Python 3.6+
- See `requirements.txt` for Python dependencies

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/network-looking-glass.git
   cd network-looking-glass
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask server:**
   ```sh
   python app.py
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:5000/
   ```

## API Endpoints

- `GET /`  
  Renders the main HTML page.

- `GET /routers/<asn>`  
  Returns a list of routers for the specified ASN.

- `POST /lg`  
  Invokes the looking glass service to run a standard or custom command on a router.  
  **Request JSON:**  
  ```json
  {
    "router": "<router_name>",
    "cmd": "<command>",         // e.g. "bgp", "ping", "traceroute", or "custom"
    "ipprefix": "<ip_prefix>",  // Only for standard commands
    "customCmd": "<custom_command>" // Only for custom commands
  }
  ```

- `POST /cmds`  
  (Currently returns test data.)

## Project Structure

- `app.py` - Main Flask application
- `ssh_client.py` - SSH client logic
- `helpers.py` - Helper functions
- `routers.py` - Router data
- `templates/index.html` - Main HTML template
- `static/js/lg.js` - Main JavaScript logic for UI interactivity

## Notes

- Make sure your SSH credentials and router information are correctly configured in the relevant files.
- The UI will hide the IP/Prefix field when "Custom Command" is selected, and show it for standard commands.
- For development, the server runs in debug mode and listens on all interfaces.

---

Feel free to contribute or open issues!