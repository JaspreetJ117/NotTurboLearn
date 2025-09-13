# -----------------------------------------------------------------------------
# Jaspreet Singh Jawanda Software License v1.0
#
# This software is licensed, not sold. All rights reserved by Jaspreet Singh Jawanda.
# The client is granted a non-exclusive, non-transferable license for internal use
# at a single corporate branch. Redistribution, reverse engineering, and sublicensing
# are strictly prohibited. For full license terms, see LICENSE.txt.
# -----------------------------------------------------------------------------

"""
packaged.py

System tray entry point for the NotTurboLearn application.

This module implements the system tray interface for Enventory, providing:

- A Pystray-based tray icon for launching and controlling the Enventory server.
- Dynamic menu actions for starting and stopping the Waitress web server, displaying local IP address, and quitting the application.
- Status notifications and error handling for server lifecycle events.
- Utility functions for loading the application logo, managing subprocesses, and reporting system status.
- Threaded server control to ensure responsive user interactions.

The architecture is designed for seamless integration with Windows and cross-platform environments, supporting both script and compiled executable modes. The module emphasizes usability, reliability, and secure server management for internal deployments.

Author: Jaspreet Jawanda
Email: jaspreetjawanda@proton.me
Version: 1.1.0
Status: Production
"""

# --- Library Imports ---
import sys
import os
import pystray
from PIL import Image, ImageDraw
import threading
import subprocess
import time
import socket

# --- Global State ---
proc = None
server_running = False
# FIX: A lock to prevent race conditions when multiple threads access global state.
server_lock = threading.Lock()


# Add project root to sys.path so 'scripts.app' can be imported by waitress
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# --- IP Address Utility ---
def get_local_ip():
    """Gets the local IP address of the machine."""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't have to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except OSError:
        ip = "127.0.0.1"
    finally:
        if s:
            s.close()
    return f"{ip}:8017"

# Get the IP once when the script starts
local_ip_address = get_local_ip()

# --- Icon Image Creation ---
def create_image():
    """Loads the logo image for the system tray icon."""
    try:
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))

        logo_path = os.path.join(base_path, 'static', 'images', 'logo.png')
        return Image.open(logo_path)
    except FileNotFoundError as e:
        print(f"Error: Logo file not found. Using fallback icon. Details: {e}")
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        draw.ellipse((width // 4, height // 4, width * 3 // 4, height * 3 // 4), fill='#1a73e8')
        return image

# --- Server Process Monitoring ---
def monitor_server_process(icon):
    """
    FIX: Runs in a separate thread, waits for the server process to exit,
    and then updates the application state. This prevents the UI from blocking.
    """
    global proc, server_running
    if proc:
        proc.wait() # This will block THIS thread until the server process terminates.
    
    with server_lock:
        server_running = False
        proc = None
    
    print("packaged.py: Server process has terminated.")
    # Update the menu to reflect the server status (e.g., re-enable 'Start Server')
    icon.update_menu()

# --- Server Control Functions (internal) ---
def start_waitress_server_thread(icon):
    """
    FIX: Starts the server and a non-blocking monitor thread. The function
    returns immediately, keeping the UI responsive.
    """
    global proc, server_running
    with server_lock:
        if not server_running:
            try:
                print("packaged.py: Starting Waitress server process...")
                # The Popen object is created without waiting for it to complete.
                proc = subprocess.Popen([
                    sys.executable, '-m', 'waitress',
                    '--listen=0.0.0.0:8017',
                    'scripts.app:app'
                ], cwd=project_root)

                server_running = True
                
                # Start the monitor thread to watch the server process in the background.
                monitor_thread = threading.Thread(target=monitor_server_process, args=(icon,), daemon=True)
                monitor_thread.start()

                print(f"packaged.py: Waitress server process launched on http://{local_ip_address}")

            except Exception as e:
                print(f"packaged.py: Error launching Waitress server: {e}")
                server_running = False
                proc = None
            
            # Update menu regardless of success or failure to reflect current state.
            icon.update_menu()

def stop_waitress_server_process(icon):
    """
    FIX: Terminates the server process without blocking. The monitor thread
    will handle the state change once the process fully exits.
    """
    global proc, server_running
    with server_lock:
        if server_running and proc:
            print("packaged.py: Stopping Waitress server process...")
            try:
                proc.terminate() # Send a termination signal.
            except Exception as e:
                print(f"packaged.py: Error stopping Waitress server: {e}")
    # The monitor thread will automatically update the UI when the process closes.

# --- Pystray Menu Item Actions ---
def start_server_action(icon):
    if not server_running:
        # We start the server in a new thread to avoid blocking the pystray event loop.
        server_thread = threading.Thread(target=start_waitress_server_thread, args=(icon,), daemon=True)
        server_thread.start()
        print("packaged.py: 'Start Server' clicked. Server initiation requested.")
    else:
        print("packaged.py: Server is already running. Action ignored.")

def stop_server_action(icon):
    if server_running:
        stop_waitress_server_process(icon)
        print("packaged.py: 'Stop Server' clicked. Server termination requested.")
    else:
        print("packaged.py: Server is not running. Action ignored.")

def on_quit_action(icon):
    print("packaged.py: 'Quit' clicked. Shutting down application...")
    stop_waitress_server_process(icon)
    icon.stop()
    print("packaged.py: Application exited.")

# --- Main Application Entry Point ---
if __name__ == "__main__":

    print("packaged.py: Initializing Pystray icon application...")

    # Create the menu items as a tuple with dynamic 'enabled' properties
    menu_items = (
        pystray.MenuItem('Enventory', None, enabled=False),
        pystray.MenuItem(f'IP Address: {local_ip_address}', None, enabled=False),
        pystray.MenuItem('Start Server', start_server_action, enabled=lambda item: not server_running),
        #pystray.MenuItem('Stop Server', stop_server_action, enabled=lambda item: server_running),
        #pystray.MenuItem('Quit', on_quit_action),
    )

    # Create the icon instance and assign the menu
    icon = pystray.Icon(
        'ENVENTORY_Server_Control',
        icon=create_image(),
        title='ENVENTORY Server Control (RGB-TOR)',
        menu=pystray.Menu(*menu_items)
    )

    print("packaged.py: Pystray icon application starting. Check your system tray.")
    # Automatically start the server on launch
    start_server_action(icon)
    
    try:
        icon.run()
    except Exception as e:
        print(f"packaged.py: An error occurred while running the icon application: {e}")
