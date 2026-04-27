"""
IT Dashboard — COP1034C Python for IT
Austin Windorski | 04/11/2026

A command-line IT management tool that grows into a full
desktop application over 4 weeks. Each class session adds
a new feature to this project.
"""

# Import network device management modules
from device_manger import Router, Switch, DeviceManager
from network_visualizer import draw_topology

# ── Application Metadata ──────────────────────────────────
APP_NAME = "IT Dashboard"
VERSION = "0.5.0"
CREATOR_NAME = "Austin Windorski"
PROF_NAME = "Prof. Frank Mora"
COURSE_NAME = "COP1034C - Python for IT"
ASSIGNMENT_NAME = "Python Project"

# Importing the current date for report timestamping
from datetime import date  # noqa: E402
today = date.today()
todaystr = today.isoformat()  # 'YYYY-MM-DD'

# String variables for server identity
server_name = "Not entered"
ip_address = "Not entered"
department = "Not entered"

# Numeric variables for disk metrics (integers in GB)
total_disk_gb = 0
used_disk_gb = 0

# Float: calculated percentage (set after user enters disk values)
usage_pct = 0.0
storage_status = "NORMAL"
# Boolean flag: True once the user has entered data
report_ready = False

# Network Device Manager instance
network_manager = DeviceManager()

# Helper function to validate IPv4 address
def is_valid_ipv4(ip):
    """Validate that a string is a valid IPv4 address."""
    import re
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(pattern, ip)
    if not match:
        return False
    # Check each octet is between 0-255
    for octet in match.groups():
        if int(octet) > 255:
            return False
    return True


def is_ip_taken(ip):
    """Check if an IP address is already in use by another device."""
    for device in network_manager.devices:
        if device.ip_address == ip:
            return True
    return False


def get_valid_ip(prompt):
    """Get a valid IPv4 address from user input."""
    while True:
        ip = input(prompt).strip()
        if not is_valid_ipv4(ip):
            print("Invalid IP address. Must be in format xxx.xxx.xxx.xxx (each octet 0-255).")
            continue
        if is_ip_taken(ip):
            print("IP address is already in use by another device.")
            continue
        return ip


def get_valid_protocol():
    """Get a valid routing protocol from user input."""
    valid_protocols = {
        'O': 'OSPF',
        'B': 'BGP',
        'E': 'EIGRP',
        'S': 'Static',
        'OSPF': 'OSPF',
        'BGP': 'BGP',
        'EIGRP': 'EIGRP',
        'STATIC': 'Static'
    }
    while True:
        protocol = input("Enter routing protocol (O=OSPF, B=BGP, E=EIGRP, S=Static): ").strip().upper()
        if protocol in valid_protocols:
            return valid_protocols[protocol]
        print("Invalid protocol. Enter O, B, E, S or full name (OSPF, BGP, EIGRP, Static).")


# Pre-load some sample devices
r1 = Router("CORE-RTR-01", "10.0.0.1", "OSPF")
s1 = Switch("ACCESS-SW-01", "10.0.0.2", 24)
r2 = Router("EDGE-RTR-01", "10.0.0.3", "BGP")
network_manager.add_device(r1)
network_manager.add_device(s1)
network_manager.add_device(r2)

# Main menu - Page 1
def print_menu_page1():
    print("\n--- IT Dashboard ---")
    print("1) Enter server info")
    print("2) View report")
    print("3) Parse log summary")
    print("M) More options...")
    print("0) Exit")

# Main menu - Page 2
def print_menu_page2():
    print("\n--- IT Dashboard (More) ---")
    print("1) Add a router")
    print("2) Add a switch")
    print("3) List all network devices")
    print("4) Draw network topology")
    print("5) Ping a device")
    print("6) Remove a device")
    print("R) Back to main menu")
    print("0) Exit")

# Collecting user input
def collect_input():
    global server_name, ip_address, department
    global total_disk_gb, used_disk_gb, usage_pct, report_ready
    global storage_usage_pct, storage_status

    server_name = input("Enter server name: ").strip()
    ip_address = input("Enter IP address: ").strip()
    department = input("Enter department: ").strip()

    try:
        total_disk_gb = int(input("Enter total disk space (GB): ").strip())
        used_disk_gb  = int(input("Enter used disk space (GB): ").strip())
    except ValueError:
        print("Invalid disk values. Please enter integers.")
        return

    # Validation
    if total_disk_gb < 0 or used_disk_gb < 0:
        print("Disk values must be non-negative.")
        report_ready = False
        return
    if used_disk_gb > total_disk_gb:
        print("Used disk cannot exceed total disk.")
        report_ready = False
        return

    # Calculate usage_pct
    if total_disk_gb == 0:
        usage_pct = 0.0
        storage_usage_pct = 0.0
    else:
        usage_pct = (used_disk_gb / total_disk_gb) * 100.0
        storage_usage_pct = (used_disk_gb / total_disk_gb) * 100.0

    # Storage status thresholds
    if storage_usage_pct >= 90.0:
        storage_status = "CRITICAL"
    elif storage_usage_pct >= 75.0:
        storage_status = "WARNING"
    else:
        storage_status = "NORMAL"

    report_ready = True
    print("Server info and disk usage recorded.")

# View the user compiled report
def view_report():
    global server_name, ip_address, department
    global total_disk_gb, used_disk_gb, usage_pct, report_ready
    global storage_status

    if not report_ready:
        print("No data entered yet. Choose option 1 first.")
        return
    # Display the report
    print("\n--- IT Report ---")
    print(f"Server Name : {server_name}")
    print(f"IP Address  : {ip_address}")
    print(f"Department  : {department}")
    print(f"Total Disk  : {total_disk_gb} GB")
    print(f"Used Disk   : {used_disk_gb} GB")
    print(f"Usage: {usage_pct:.2f}% ({storage_status})")
    print("------------------")
# Log parsing function to extract date, severity, and message from a log line
def parse_line(line):
    import re
    m = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)$', line)
    if not m:
        return None
    date_field, severity, message = m.groups()
    return {'date': date_field, 'severity': severity, 'message': message}

# Log parser function to read server.log, summarize severity counts, unique errors, and critical events
def run_log_parser():
    import os
    global severity_counts, unique_errors, critical_events, log_entries
    severity_counts = {}
    unique_errors = set()
    critical_events = set()
    log_entries = []
    # Read the log file and process each line
    try:
        logfile = os.path.join(os.path.dirname(__file__), 'server.log')
        with open(logfile, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                entry = parse_line(line)
                if not entry:
                    continue
                severity = entry['severity']
                message = entry['message']
                date_field = entry['date']

                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                if severity == "ERROR":
                    unique_errors.add(message)
                if severity == "CRITICAL":
                    critical_events.add(message)

                log_entries.append({'date': date_field, 'severity': severity, 'message': message})
    except FileNotFoundError:
        print("Error: server.log not found. Place server.log in the same directory as this script.")
        return

    total_lines = len(log_entries)
    error_count = severity_counts.get("ERROR", 0)
    error_rate = (error_count / total_lines) * 100.0 if total_lines > 0 else 0.0

    header_lines = []
    for level in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        count = severity_counts.get(level, 0)
        header_lines.append(f"{level:<9}: {count:>4}")
    header_section = "\n".join(header_lines)

    # Write the summary report to log_summary.txt
    with open(os.path.join(os.path.dirname(__file__), 'log_summary.txt'), 'w') as out:
        print("=" * 37, file=out)
        print(f"{APP_NAME} v{VERSION}", file=out)
        print(f"{CREATOR_NAME} | {PROF_NAME}", file=out)
        print(f"{COURSE_NAME} | {today}", file=out)
        print("=" * 37, file=out)
        # Append the log summary details
        print(header_section, file=out)
        print(f"\nError rate: {error_rate:.2f}%", file=out)
        print("Unique ERROR messages: {}".format(len(unique_errors)), file=out)
        print("CRITICAL events: {}".format(len(critical_events)), file=out)
        # Append unique error messages and critical events
        print("\n" + "=" * 37, file=out)
        print(f"{'UNIQUE ERROR MESSAGES':^36}", file=out)
        print("-" * 37, file=out)
        if unique_errors:
            for err in sorted(unique_errors):
                print(f"- {err}", file=out)
        else:
            print("(none)", file=out)

        print("\n" + "=" * 37, file=out)
        print(f"{'UNIQUE CRITICAL MESSAGES':^36}", file=out)
        print("-" * 37, file=out)
        if critical_events:
            for c in sorted(critical_events):
                print(f"- {c}", file=out)
        else:
            print("(none)", file=out)


# Network device management functions
def add_router_menu():
    """Add a router to the network manager."""
    hostname = input("Enter router hostname: ").strip()
    ip_address = get_valid_ip("Enter router IP address: ")
    protocol = get_valid_protocol()
    router = Router(hostname, ip_address, routing_protocol=protocol)
    network_manager.add_device(router)
    print(f"Router '{hostname}' added successfully.")


def add_switch_menu():
    """Add a switch to the network manager."""
    hostname = input("Enter switch hostname: ").strip()
    ip_address = get_valid_ip("Enter switch IP address: ")
    try:
        port_count = int(input("Enter port count (24 or 48): ").strip())
    except ValueError:
        port_count = 24
        print("Invalid port count, using default 24.")
    switch = Switch(hostname, ip_address, port_count=port_count)
    network_manager.add_device(switch)
    print(f"Switch '{hostname}' added successfully.")


def list_network_devices():
    """List all network devices - demonstrates polymorphism."""
    network_manager.list_all()


def draw_topology_menu():
    """Draw the network topology using turtle graphics."""
    if not network_manager.devices:
        print("No devices to draw. Add some devices first.")
        return
    print("Opening turtle graphics window... Close it to continue.")
    try:
        draw_topology(network_manager)
    except Exception as e:
        print(f"Topology window closed: {e}")


def ping_device_menu():
    """Ping a network device by hostname."""
    hostname = input("Enter hostname to ping: ").strip()
    device = network_manager.find_device(hostname)
    if device:
        print(f"Pinging {hostname} ({device.ip_address})...")
        result = device.ping()
        print(result)
    else:
        print(f"Device '{hostname}' not found.")


def remove_device_menu():
    """Remove a network device by hostname."""
    hostname = input("Enter hostname to remove: ").strip()
    network_manager.remove_device(hostname)

# Defining the main app
def main():
    print("=" * 37)
    print(f"{APP_NAME} v{VERSION}")
    print()
    print(f"{CREATOR_NAME} | {PROF_NAME}")
    print(f"{COURSE_NAME} | {today}")
    print("Ready to build something great.")
    print("\nPre-loaded 3 sample network devices.")
    print("=" * 37)

    # Main loop - Page 1
    while True:
        print_menu_page1()
        choice = input("Select an option: ").strip().upper()
        if choice == "1":
            collect_input()
        elif choice == "2":
            view_report()
        elif choice == "3":
            run_log_parser()   # only here will logsummary.txt be created
        elif choice == "M":
            # Go to Page 2
            while True:
                print_menu_page2()
                choice = input("Select an option: ").strip().upper()
                if choice == "1":
                    add_router_menu()
                elif choice == "2":
                    add_switch_menu()
                elif choice == "3":
                    list_network_devices()
                elif choice == "4":
                    draw_topology_menu()
                elif choice == "5":
                    ping_device_menu()
                elif choice == "6":
                    remove_device_menu()
                elif choice == "R":
                    break  # Back to Page 1
                elif choice == "0":
                    print("Goodbye. Application shutting down.")
                    return
                else:
                    print("Invalid choice. Enter 1-6, R, or 0.")
        elif choice == "0":
            print("Goodbye. Application shutting down.")
            break
        else:
            print("Invalid choice. Enter 1-3, M, or 0.")

# Run the program
if __name__ == "__main__":
    main()