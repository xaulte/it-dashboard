"""
IT Dashboard — COP1034C Python for IT
Austin Windorski | 04/11/2026

GUI Application Entry Point
"""

import tkinter as tk
from device_manger import Router, Switch, DeviceManager
from gui_dashboard import ITDashboardGUI

def main():
    # Setup Network Device Manager with sample data
    network_manager = DeviceManager()
    network_manager.add_device(Router("CORE-RTR-01", "10.0.0.1", "OSPF"))
    network_manager.add_device(Switch("ACCESS-SW-01", "10.0.0.2", 24))
    network_manager.add_device(Router("EDGE-RTR-01", "10.0.0.3", "BGP"))

    # Launch GUI
    root = tk.Tk()
    app = ITDashboardGUI(root, network_manager)
    root.mainloop()

if __name__ == "__main__":
    main()