"""
Server Status Tool | COP1034C - Python for IT
Austin Windorski | 04/11/2026

"""
import tkinter as tk
from tkinter import messagebox
import psutil
import socket

# Main application window
root = tk.Tk()
root.title("Server Status Tool")
root.geometry("450x350")
root.resizable(False, False)
root.configure(bg="#1a1a2e")

# Program title label
title_label = tk.Label(
    root,
    text="Server Status Tool",
    font=("Arial", 18, "bold"),
    fg="#c9a83a",       # gold text
    bg="#1a1a2e"        # match window background
)
title_label.pack(pady=15)

# Frame to hold the input row
input_frame = tk.Frame(root, bg="#1a1a2e")
input_frame.pack(pady=10)

ip_label = tk.Label(
    input_frame, text="Server IP:",
    font=("Arial", 11), fg="white", bg="#1a1a2e"
)
ip_label.grid(row=0, column=0, padx=5)

ip_entry = tk.Entry(input_frame, width=25, font=("Consolas", 11))
ip_entry.grid(row=0, column=1, padx=5)
ip_entry.insert(0, "192.168.1.1")  # default value

# Define the function FIRST
def check_status():
    ip = ip_entry.get()
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Checking {ip}...\n")
    result_text.insert(tk.END, f"Status: ONLINE\n")
    result_text.insert(tk.END, f"Response: 12ms\n")

# Then create the button that calls it
check_btn = tk.Button(
    root, text="Check Status",
    command=check_status,   # NO parentheses!
    font=("Arial", 11, "bold"),
    bg="#c9a83a", fg="#000",
    cursor="hand2", width=15
)
check_btn.pack(pady=10)

result_text = tk.Text(
    root, width=50, height=8,
    font=("Consolas", 10),
    bg="#0d1117", fg="#3ab577",  # dark bg, green text
    relief="sunken"              # inset border style
)
result_text.pack(padx=20, pady=5)

status_var = tk.StringVar(value="Ready")

status_bar = tk.Label(
    root, textvariable=status_var,
    font=("Arial", 9),
    fg="#64748b", bg="#12121e",
    anchor="w",  # left-align text
    padx=10
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Update your check_status function to use it:
def check_status():
    ip = ip_entry.get()
    status_var.set(f"Checking {ip}...")  # status bar updates!
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Checking {ip}...\n")
    result_text.insert(tk.END, f"Status: ONLINE\n")
    status_var.set(f"Last checked: {ip}")

# Add a function to clear results and reset status
def clear_results():
    result_text.delete("1.0", tk.END)
    ip_entry.delete(0, tk.END)
    status_var.set("Cleared")

# Add a button frame for side-by-side buttons
btn_frame = tk.Frame(root, bg="#1a1a2e")
btn_frame.pack(pady=10)

# Create the Check Status button
check_btn = tk.Button(
    btn_frame, text="Check Status",
    command=check_status, bg="#c9a83a", fg="#000",
    font=("Arial", 11, "bold"), width=15, cursor="hand2"
)
check_btn.grid(row=0, column=0, padx=5)

# Create the Clear button next to Check Status
clear_btn = tk.Button(
    btn_frame, text="Clear",
    command=clear_results, bg="#374151", fg="white",
    font=("Arial", 11), width=10, cursor="hand2"
)
clear_btn.grid(row=0, column=1, padx=5)

# Update check_status to validate first:
def check_status():
    ip = ip_entry.get().strip()
    if not ip:
        messagebox.showerror("Error", "Please enter a server IP address.")
        return
    status_var.set(f"Checking {ip}...")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Checking {ip}...\n")
    result_text.insert(tk.END, f"Status: ONLINE\n")
    result_text.insert(tk.END, f"Response: 12ms\n")
    status_var.set(f"Last checked: {ip}")

    # bind() needs a function that accepts an event parameter
def on_enter_key(event):
    check_status()

# Bind the Enter key to the entry widget
ip_entry.bind("<Return>", on_enter_key)

#Run the program
root.mainloop()