"""
IT Dashboard — COP1034C Python for IT
Austin Windorski | 04/11/2026

A command-line IT management tool that grows into a full
desktop application over 4 weeks. Each class session adds
a new feature to this project.
"""

# ── Application Metadata ──────────────────────────────────
APP_NAME = "IT Dashboard"
VERSION = "0.2.0"

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

def print_menu():
    print("\n--- IT Report Generator ---")
    print("1) Enter server info")
    print("2) View report")
    print("3) Exit")

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
    elif storage_usage_pct >= 70.0:
        storage_status = "WARNING"
    else:
        storage_status = "NORMAL"

    report_ready = True
    print("Server info and disk usage recorded.")

def view_report():
    global server_name, ip_address, department
    global total_disk_gb, used_disk_gb, usage_pct, report_ready
    global storage_status

    if not report_ready:
        print("No data entered yet. Choose option 1 first.")
        return

    print("\n--- IT Report ---")
    print(f"Server Name : {server_name}")
    print(f"IP Address  : {ip_address}")
    print(f"Department  : {department}")
    print(f"Total Disk  : {total_disk_gb} GB")
    print(f"Used Disk   : {used_disk_gb} GB")
    print(f"Usage: {usage_pct:.2f}% ({storage_status})")
    print("------------------")

def main():
    print(f"{APP_NAME} v{VERSION}")
    print("Ready to build something great.")
    while True:
        print_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            collect_input()
        elif choice == "2":
            view_report()
        elif choice == "3":
            print("Goodbye. Application shutting down.")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

# Run the program
if __name__ == "__main__":
    main()