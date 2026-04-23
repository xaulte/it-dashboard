"""
IT Dashboard — COP1034C Python for IT
Austin Windorski | 04/11/2026

A command-line IT management tool that grows into a full
desktop application over 4 weeks. Each class session adds
a new feature to this project.
"""

# ── Application Metadata ──────────────────────────────────
APP_NAME = "IT Dashboard"
VERSION = "0.3.0"
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

# Main menu
def print_menu():
    print("\n--- IT Report Generator ---")
    print("1) Enter server info")
    print("2) View report")
    print("3) Parse log summary")
    print("4) Exit")

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


# Defining the main app
def main():
    print(f"{APP_NAME} v{VERSION}")
    print(f"{today}")
    print(f"{CREATOR_NAME} | {PROF_NAME}")
    print(f"{COURSE_NAME} | {ASSIGNMENT_NAME}")
    print("Ready to build something great.")

    # Main loop
    while True:
        print_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            collect_input()
        elif choice == "2":
            view_report()
        elif choice == "3":
            run_log_parser()   # only here will logsummary.txt be created
        elif choice == "4":
            print("Goodbye. Application shutting down.")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")

# Run the program
if __name__ == "__main__":
    main()