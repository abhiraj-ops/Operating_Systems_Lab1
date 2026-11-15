"""
Lab 3 - Q4: Device allocation.

Covers:
  * dedicated devices (a printer) - one process owns the device at a time,
    the other processes wait in a queue and the owner hands the device over
    to the first process in the queue when it is released;
  * shared devices (a disk) - every request is queued and served one after
    the other;
  * virtual devices (a virtual printer) - the requests are queued as well;
  * a bounded buffer (buffering of device data).

Run with:  python3 src/device_allocation.py
"""

from collections import deque


class Device:
    """A device that is either dedicated, shared or virtual."""

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        self.owner = None
        self.queue = deque()

    def request(self, process):
        """A process asks for the device."""
        if self.kind == "dedicated":
            if self.owner is None:
                self.owner = process
                return f"{process} allocated {self.name}"
            self.queue.append(process)
            return f"{process} queued for {self.name}"
        self.queue.append(process)
        return f"{process} submitted request to {self.name}"

    def release(self, process):
        """A process gives a dedicated device back."""
        if self.kind != "dedicated":
            return "Release operation applies to dedicated devices only"
        if self.owner != process:
            return f"{process} does not own {self.name}"
        self.owner = None
        message = f"{process} released {self.name}"
        if self.queue:
            self.owner = self.queue.popleft()
            message += f"; {self.owner} is now owner"
        return message

    def service_next(self):
        """Serve the oldest pending request of the device."""
        if not self.queue:
            return f"No pending request for {self.name}"
        process = self.queue.popleft()
        return f"{self.name} served {process}"


class Buffer:
    """A fixed size buffer holding the data of a device."""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Buffer capacity must be positive")
        self.capacity = capacity
        self.items = deque()

    def put(self, item):
        """Insert an item, unless the buffer is already full."""
        if len(self.items) >= self.capacity:
            return "Buffer full"
        self.items.append(item)
        return f"Inserted {item}"

    def get(self):
        """Remove the oldest item, unless the buffer is empty."""
        if not self.items:
            return "Buffer empty"
        return f"Removed {self.items.popleft()}"


printer = Device("Printer", "dedicated")
disk = Device("SharedDisk", "shared")
virtual = Device("VirtualPrinter", "virtual")

print(printer.request("P1"))
print(printer.request("P2"))
print(printer.release("P1"))
print(disk.request("P3"))
print(disk.request("P4"))
print(disk.service_next())
print(disk.service_next())
print(virtual.request("P5"))
print(virtual.service_next())

buffer = Buffer(3)
for item in ["A", "B", "C", "D"]:
    print(buffer.put(item), list(buffer.items))
for _ in range(4):
    print(buffer.get(), list(buffer.items))
