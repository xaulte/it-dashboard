class NetworkDevice:
    """Base class representing a generic network device.

    Attributes:
        hostname    (str)  : device hostname, e.g. CORE-RTR-01
        ip_address  (str)  : IPv4 address, e.g. 10.0.0.1
        device_type (str)  : 'router', 'switch', etc.
        status      (str)  : 'online' or 'offline'
    """

    def __init__(self, hostname, ip_address, device_type, status="online"):
        """Initialize a NetworkDevice with identity and status fields."""
        # Assign parameters to instance attributes
        self.hostname = hostname
        self.ip_address = ip_address
        self.device_type = device_type
        self.status = status

    def __str__(self):
        """Return a one-line summary string for this device."""
        # Return an f-string: "[device_type] hostname | ip_address | Status: status"
        return f"[{self.device_type}] {self.hostname} | {self.ip_address} | Status: {self.status}"

    def ping(self):
        """Simulate a ping to this device and return a result string."""
        # Return a string like: "Reply from 10.0.0.1: bytes=32 time=2ms TTL=64"
        import random
        time_ms = random.randint(1, 10)
        ttl = random.randint(60, 128)
        return f"Reply from {self.ip_address}: bytes=32 time={time_ms}ms TTL={ttl}"

    def get_info(self):
        """Return a formatted string with this device's details."""
        # Base version: return hostname, ip, type, and status
        return f"Hostname: {self.hostname}\nIP Address: {self.ip_address}\nDevice Type: {self.device_type}\nStatus: {self.status}"

    def set_status(self, new_status):
        """Update the device status to the given string."""
        self.status = new_status

class Router(NetworkDevice):
    """A network router. Extends NetworkDevice with routing information.

    Additional Attributes:
        routing_protocol (str)  : e.g. 'OSPF', 'BGP', 'EIGRP', 'Static'
        routes           (list) : list of route strings in CIDR notation
    """

    def __init__(self, hostname, ip_address, routing_protocol="OSPF"):
        """Initialize a Router — calls super().__init__ with device_type='router'."""
        # Call the parent constructor — device_type is always 'router' for this class
        super().__init__(hostname, ip_address, device_type="router")
        self.routing_protocol = routing_protocol
        # Start with an empty routes list — populated by show_routes()
        self.routes = []

    def get_info(self):
        """Override base get_info to include routing protocol and routes."""
        # Call str(self) for the base summary line, then append protocol and routes
        base_info = str(self)
        routes_info = "\n".join(self.routes) if self.routes else "(no routes)"
        return f"{base_info}\nRouting Protocol: {self.routing_protocol}\nRoutes:\n{routes_info}"

    def show_routes(self):
        """Return a list of routes this router knows about.

        In a real tool this would query the device. Here, return a
        simulated list of CIDR strings appropriate for the routing protocol.
        """
        # Simulate routes based on routing protocol
        if self.routing_protocol == "OSPF":
            self.routes = ["192.168.1.0/24", "10.0.0.0/8", "172.16.0.0/12"]
        elif self.routing_protocol == "BGP":
            self.routes = ["203.0.113.0/24", "198.51.100.0/24"]
        elif self.routing_protocol == "EIGRP":
            self.routes = ["192.168.10.0/24", "10.10.0.0/16"]
        else:  # Static or default
            self.routes = ["0.0.0.0/0", "192.168.1.0/24"]
        return self.routes

    def add_route(self, route):
        """Add a route string to this router's route list."""
        self.routes.append(route)

class Switch(NetworkDevice):
    """A network switch. Extends NetworkDevice with VLAN and port information.

    Additional Attributes:
        port_count (int)  : number of switchports (e.g. 24 or 48)
        vlans      (list) : list of VLAN description strings
    """

    def __init__(self, hostname, ip_address, port_count=24):
        """Initialize a Switch — calls super().__init__ with device_type='switch'."""
        super().__init__(hostname, ip_address, device_type="switch")
        self.port_count = port_count
        self.vlans = ["VLAN 1 (default)"]  # every switch starts with VLAN 1

    def get_info(self):
        """Override base get_info to include port count and VLAN list."""
        base_info = str(self)
        vlans_info = "\n".join(self.vlans) if self.vlans else "(no VLANs)"
        return f"{base_info}\nPort Count: {self.port_count}\nVLANs:\n{vlans_info}"

    def show_vlans(self):
        """Return the current list of VLAN description strings."""
        return self.vlans

    def add_vlan(self, vlan_description):
        """Add a VLAN description string to this switch's VLAN list."""
        self.vlans.append(vlan_description)

class DeviceManager:
    """Manages a collection of NetworkDevice objects.

    Provides add, remove, find, and list operations over
    the internal devices list.
    """

    def __init__(self):
        """Initialize with an empty device list."""
        self.devices = []

    def add_device(self, device):
        """Add a NetworkDevice (or subclass) to the devices list."""
        self.devices.append(device)

    def remove_device(self, hostname):
        """Remove the device with the given hostname. Print a message if not found."""
        # Normalize: lowercase and replace underscores with hyphens
        hostname_normalized = hostname.lower().replace('_', '-')
        for i, device in enumerate(self.devices):
            device_normalized = device.hostname.lower().replace('_', '-')
            if device_normalized == hostname_normalized:
                self.devices.pop(i)
                print(f"Device '{hostname}' removed successfully.")
                return
        print(f"Device '{hostname}' not found.")

    def find_device(self, hostname):
        """Return the device object matching hostname, or None if not found."""
        # Normalize: lowercase and replace underscores with hyphens
        hostname_normalized = hostname.lower().replace('_', '-')
        for device in self.devices:
            device_normalized = device.hostname.lower().replace('_', '-')
            if device_normalized == hostname_normalized:
                return device
        return None

    def list_all(self):
        """ Print the get_info() output for every device in the list.
           This is the polymorphism loop — call get_info() on each device
            regardless of whether it is a Router or Switch """
        if not self.devices:
            print("No devices in manager.")
            return
        for device in self.devices:
            print(device.get_info())
            print("-" * 40)