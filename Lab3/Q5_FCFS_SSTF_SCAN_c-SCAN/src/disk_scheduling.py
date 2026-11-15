"""
Lab 3 - Q5: Disk scheduling (FCFS, SSTF, SCAN and C-SCAN).

Covers:
  * FCFS  - the requests are served in the order they arrive;
  * SSTF  - the closest request is served next;
  * SCAN  - the head moves in one direction up to the end of the disk and
            then continues in the opposite direction (the requests are
            served on the way back as well);
  * C-SCAN - the head moves in one direction only; after reaching the end of
            the disk it returns to the beginning without serving requests;
  * the swap space of a process is managed with a block bitmap, which is
            the backing store of the swapping done in Q1.

For every algorithm the head movement is printed together with the average
movement per request.

Run with:  python3 src/disk_scheduling.py
"""


def validate(requests, head, minimum, maximum):
    """The head and every request must lie inside the disk range."""
    if minimum < 0 or maximum <= minimum:
        raise ValueError("Invalid disk range")
    if not minimum <= head <= maximum:
        raise ValueError("Head outside disk range")
    if any(not minimum <= request <= maximum for request in requests):
        raise ValueError("Request outside disk range")


def movement(path):
    """Total head movement of a path."""
    return sum(abs(path[i] - path[i - 1]) for i in range(1, len(path)))


def fcfs(requests, head):
    """Serve the requests in the order they were issued."""
    return [head] + requests[:]


def sstf(requests, head):
    """Always serve the request that is closest to the current head position."""
    pending = requests[:]
    path = [head]
    current = head

    while pending:
        next_request = min(pending, key=lambda value: (abs(value - current), value))
        path.append(next_request)
        pending.remove(next_request)
        current = next_request

    return path


def scan(requests, head, minimum, maximum, direction="right"):
    """Servicing in one direction, then in the opposite one."""
    left = sorted(
        [request for request in requests if request < head], reverse=True
    )
    right = sorted([request for request in requests if request >= head])

    if direction == "right":
        return [head] + right + [maximum] + left
    return [head] + left + [minimum] + right


def cscan(requests, head, minimum, maximum):
    """Servicing in one direction only - the head returns without serving."""
    left = sorted([request for request in requests if request < head])
    right = sorted([request for request in requests if request >= head])

    return [head] + right + [maximum, minimum] + left


class SwapSpace:
    """Swap space of a machine, managed with a block bitmap."""

    def __init__(self, blocks):
        if blocks <= 0:
            raise ValueError("Swap block count must be positive")
        self.bitmap = [0] * blocks
        self.allocations = {}

    def allocate(self, process, count):
        """Give `count` free swap blocks to a process."""
        if count <= 0:
            return False
        free = [i for i, value in enumerate(self.bitmap) if value == 0]
        if len(free) < count:
            return False
        chosen = free[:count]
        for block in chosen:
            self.bitmap[block] = 1
        self.allocations[process] = chosen
        return True

    def release(self, process):
        """Give the swap blocks of a process back to the system."""
        if process not in self.allocations:
            return False
        for block in self.allocations.pop(process):
            self.bitmap[block] = 0
        return True


requests = [98, 183, 37, 122, 14, 124, 65, 67]
head = 53
minimum = 0
maximum = 199

validate(requests, head, minimum, maximum)

algorithms = {
    "FCFS": fcfs(requests, head),
    "SSTF": sstf(requests, head),
    "SCAN": scan(requests, head, minimum, maximum, "right"),
    "C-SCAN": cscan(requests, head, minimum, maximum),
}

for name, path in algorithms.items():
    total = movement(path)
    print(f"\n{name}")
    print("Path:", path)
    print("Total movement:", total)
    print("Average per request:", round(total / len(requests), 2))

swap = SwapSpace(10)
print("\nAllocate P1:", swap.allocate("P1", 4), swap.bitmap)
print("Allocate P2:", swap.allocate("P2", 5), swap.bitmap)
print("Allocate P3:", swap.allocate("P3", 3), swap.bitmap)
print("Release P1:", swap.release("P1"), swap.bitmap)
