"""
Network Visualizer — COP1034C Python for IT
Austin Windorski | 04/11/2026
Module to visualize network topology using turtle graphics.
Provides a function to draw devices from the DeviceManager in a simple layout.
"""
import turtle

def draw_topology(manager):
    """Drawing a simple network topology using turtle.

    Each device is drawn as a rectangle with its hostname
    labeled below it. Devices are spaced evenly across the screen.
    """
    screen = turtle.Screen()
    screen.title("Network Topology")
    screen.bgcolor("#0a0e1a")  # match the dark theme

    t = turtle.Turtle()
    t.speed(0)         # 0 = fastest, no animation delay
    t.hideturtle()

    # Starting x position for the first device
    x_start = -200
    x_step = 150   # horizontal gap between devices
    y_pos = 0

    for i, device in enumerate(manager.devices):
        x = x_start + (i * x_step)

        # Move to position without drawing
        t.penup()
        t.goto(x, y_pos)
        t.pendown()

        # Choose color by device type
        if device.device_type == "router":
            t.fillcolor("#10b981")  # green for routers
        else:
            t.fillcolor("#3b82f6")  # blue for switches

        # Draw a 60x40 rectangle
        t.begin_fill()
        for _ in range(2):
            t.forward(60)
            t.left(90)
            t.forward(40)
            t.left(90)
        t.end_fill()

        # Write the hostname label below the shape
        t.penup()
        t.goto(x + 30, y_pos - 20)
        t.color("white")
        t.write(device.hostname, align="center", font=("Arial", 9, "normal"))

    # Keep the window open until the user closes it
    try:
        turtle.done()
    except turtle.Terminator:
        pass  # User closed the window