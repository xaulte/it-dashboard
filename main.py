"""
IT Dashboard — COP1034C Python for IT
Austin Windorski | 04/11/2026

A command-line IT management tool that grows into a full
desktop application over 4 weeks. Each class session adds
a new feature to this project.
"""

# ── Application Metadata ──────────────────────────────────
APPNAME = "IT Dashboard"
VERSION = "0.2.0"

# String variables for server identity
servername = "Not entered"
ipaddress = "Not entered"
department = "Not entered"

# Numeric variables for disk metrics (integers in GB)
totaldiskgb = 0
useddiskgb = 0

# Float: calculated percentage (set after user enters disk values)
usagepct = 0.0

# Boolean flag: True once the user has entered data
reportready = False

def printmenu():
    print("\n--- IT Report Generator ---")
    print("1) Enter server info")
    print("2) View report")
    print("3) Exit")

def collectinput():
    global servername, ipaddress, department
    global totaldiskgb, useddiskgb, usagepct, reportready

    servername = input("Enter server name: ").strip()
    ipaddress = input("Enter IP address: ").strip()
    department = input("Enter department: ").strip()

    try:
        totaldiskgb = int(input("Enter total disk space (GB): ").strip())
        useddiskgb  = int(input("Enter used disk space (GB): ").strip())
    except ValueError:
        print("Invalid disk values. Please enter integers.")
        return

    # Validation
    if totaldiskgb < 0 or useddiskgb < 0:
        print("Disk values must be non-negative.")
        reportready = False
        return
    if useddiskgb > totaldiskgb:
        print("Used disk cannot exceed total disk.")
        reportready = False
        return

    # Calculate usagepct
    if totaldiskgb == 0:
        usagepct = 0.0
    else:
        usagepct = (useddiskgb / totaldiskgb) * 100.0

    reportready = True
    print("Server info and disk usage recorded.")

def viewreport():
    global servername, ipaddress, department
    global totaldiskgb, useddiskgb, usagepct, reportready

    if not reportready:
        print("No data entered yet. Choose option 1 first.")
        return

    print("\n--- IT Report ---")
    print(f"Server Name : {servername}")
    print(f"IP Address  : {ipaddress}")
    print(f"Department  : {department}")
    print(f"Total Disk  : {totaldiskgb} GB")
    print(f"Used Disk   : {useddiskgb} GB")
    print(f"Usage       : {usagepct:.2f}%")
    print("------------------")

def main():
    print(f"{APPNAME} v{VERSION}")
    print("Ready to build something great.")
    while True:
        printmenu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            collectinput()
        elif choice == "2":
            viewreport()
        elif choice == "3":
            print("Goodbye. Application shutting down.")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

# Run the program
if __name__ == "__main__":
    main()