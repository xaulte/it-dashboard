import tkinter as tk
from tkinter import ttk, messagebox
import os
import ipaddress
from device_manger import Router, Switch
from network_visualizer import draw_topology
import log_parser

"""
IT Dashboard GUI — COP1034C Python for IT
Austin Windorski | 04/11/2026
Graphical User Interface for IT Dashboard using Tkinter
Provides tabs for Server Info, Network Devices, and Log Parsing
"""

class ITDashboardGUI:
    def __init__(self, root, network_manager):
        self.root = root
        self.manager = network_manager
        
        self.root.title("IT Dashboard v0.6.0")
        self.root.geometry("650x550")
        self.root.configure(bg="#1a1a2e")

        # Configure styling to match your dark theme
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab', background='#374151', foreground='white', padding=[15, 5])
        style.map('TNotebook.Tab', background=[('selected', '#c9a83a')], foreground=[('selected', 'black')])
        
        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=15, pady=15)

        # Tab Frames
        self.tab_server = tk.Frame(self.notebook, bg="#1a1a2e")
        self.tab_network = tk.Frame(self.notebook, bg="#1a1a2e")
        self.tab_logs = tk.Frame(self.notebook, bg="#1a1a2e")

        self.notebook.add(self.tab_server, text="Server Info")
        self.notebook.add(self.tab_network, text="Network Devices")
        self.notebook.add(self.tab_logs, text="Log Parser")

        self.build_server_tab()
        self.build_network_tab()
        self.build_logs_tab()

    # ─── HELPER: IP VALIDATION ──────────────────────────────────────────
    def get_valid_ip_cli(self, prompt_text):
        """Loops using input() until a valid IPv4 address is provided."""
        while True:
            ip_str = input(prompt_text).strip()
            try:
                # Validates the IP format
                ipaddress.ip_address(ip_str)
                return ip_str 
            except ValueError:
                print("  [!] Error: Invalid IP address format. Please try again.")

    # ─── TAB 1: SERVER INFO ─────────────────────────────────────────────
    def build_server_tab(self):
        form_frame = tk.Frame(self.tab_server, bg="#1a1a2e")
        form_frame.pack(pady=20)

        fields = ["Server Name:", "IP Address:", "Department:", "Total Disk (GB):", "Used Disk (GB):"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(form_frame, text=field, fg="white", bg="#1a1a2e", font=("Arial", 11)).grid(row=i, column=0, sticky="e", padx=10, pady=8)
            ent = tk.Entry(form_frame, font=("Consolas", 11), width=25)
            ent.grid(row=i, column=1, padx=10, pady=8)
            self.entries[field] = ent

        btn = tk.Button(self.tab_server, text="Generate Report", command=self.generate_report, 
                        bg="#c9a83a", fg="black", font=("Arial", 11, "bold"), cursor="hand2", width=20)
        btn.pack(pady=10)

        self.server_result = tk.Text(self.tab_server, width=60, height=8, bg="#0d1117", fg="#3ab577", font=("Consolas", 10), relief="sunken")
        self.server_result.pack(pady=10)

    def generate_report(self):
        try:
            name = self.entries["Server Name:"].get()
            ip = self.entries["IP Address:"].get()
            dept = self.entries["Department:"].get()
            total = int(self.entries["Total Disk (GB):"].get())
            used = int(self.entries["Used Disk (GB):"].get())

            if total < 0 or used < 0 or used > total:
                raise ValueError("Invalid disk metrics.")

            # Validate the Server Info IP (using ipaddress without a loop since it's an Entry box)
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                messagebox.showerror("Error", "Invalid Server IP Address format.")
                return

            usage_pct = (used / total) * 100.0 if total > 0 else 0.0
            status = "CRITICAL" if usage_pct >= 90 else "WARNING" if usage_pct >= 75 else "NORMAL"

            report = "--- IT Report ---\n"
            report += f"Server Name : {name}\nIP Address  : {ip}\nDepartment  : {dept}\n"
            report += f"Total Disk  : {total} GB\nUsed Disk   : {used} GB\n"
            report += f"Usage       : {usage_pct:.2f}% ({status})\n"

            self.server_result.delete("1.0", tk.END)
            self.server_result.insert(tk.END, report)
        except ValueError:
            messagebox.showerror("Error", "Please ensure disk values are valid integers and used <= total.")

    # ─── TAB 2: NETWORK DEVICES ─────────────────────────────────────────
    def build_network_tab(self):
        self.dev_listbox = tk.Listbox(self.tab_network, width=70, height=10, bg="#0d1117", fg="white", font=("Consolas", 10))
        self.dev_listbox.pack(pady=15)
        self.refresh_device_list()

        btn_frame = tk.Frame(self.tab_network, bg="#1a1a2e")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Router", command=self.add_router, bg="#3b82f6", fg="white", width=12).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Add Switch", command=self.add_switch, bg="#10b981", fg="white", width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Ping", command=self.ping_device, bg="#c9a83a", fg="black", width=10).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Draw Topology", command=self.draw_topo, bg="#8b5cf6", fg="white", width=15).grid(row=0, column=3, padx=5)

        self.net_result = tk.Text(self.tab_network, width=70, height=4, bg="#0d1117", fg="#3ab577", font=("Consolas", 10))
        self.net_result.pack(pady=10)

    def refresh_device_list(self):
        self.dev_listbox.delete(0, tk.END)
        for dev in self.manager.devices:
            self.dev_listbox.insert(tk.END, f"[{dev.device_type.upper()}] {dev.hostname} - {dev.ip_address}")

    def add_router(self):
        # Alert the user to look at the terminal
        messagebox.showinfo("Action Required", "Please check your terminal/console to enter the new router details.")
        
        print("\n--- Add New Router ---")
        hostname = input("  Enter router hostname: ").strip()
        if hostname:
            valid_ip = self.get_valid_ip_cli("  Enter IP address (e.g., 192.168.1.1): ")
            self.manager.add_device(Router(hostname, valid_ip, "OSPF"))
            self.refresh_device_list()
            print(f"[+] Successfully added Router '{hostname}' at {valid_ip}")

    def add_switch(self):
        # Alert the user to look at the terminal
        messagebox.showinfo("Action Required", "Please check your terminal/console to enter the new switch details.")
        
        print("\n--- Add New Switch ---")
        hostname = input("  Enter switch hostname: ").strip()
        if hostname:
            valid_ip = self.get_valid_ip_cli("  Enter IP address (e.g., 10.0.0.2): ")
            self.manager.add_device(Switch(hostname, valid_ip, 24))
            self.refresh_device_list()
            print(f"[+] Successfully added Switch '{hostname}' at {valid_ip}")

    def ping_device(self):
        selection = self.dev_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a device to ping.")
            return
        device = self.manager.devices[selection[0]]
        self.net_result.delete("1.0", tk.END)
        self.net_result.insert(tk.END, f"Pinging {device.hostname}...\n{device.ping()}")

    def draw_topo(self):
        if not self.manager.devices:
            messagebox.showinfo("Info", "No devices to draw.")
            return
        try:
            draw_topology(self.manager)
        except Exception as e:
            pass # Handle turtle window closure gracefully

    # ─── TAB 3: LOG PARSER ──────────────────────────────────────────────
    def build_logs_tab(self):
        btn = tk.Button(self.tab_logs, text="Parse server.log", command=self.parse_logs, 
                        bg="#c9a83a", fg="black", font=("Arial", 11, "bold"), cursor="hand2", width=20)
        btn.pack(pady=15)

        self.log_result = tk.Text(self.tab_logs, width=75, height=22, bg="#0d1117", fg="#3ab577", font=("Consolas", 9), relief="sunken")
        self.log_result.pack(pady=5)

    def parse_logs(self):
        log_path = os.path.join(os.path.dirname(__file__), 'server.log')
        out_path = os.path.join(os.path.dirname(__file__), 'log_summary.txt')
        
        status = log_parser.run_parser(log_path, out_path)
        
        self.log_result.delete("1.0", tk.END)
        if "Error" in status:
            self.log_result.insert(tk.END, status)
        else:
            with open(out_path, 'r') as f:
                self.log_result.insert(tk.END, f.read())