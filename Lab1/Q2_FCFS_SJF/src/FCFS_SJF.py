from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    completion: int = 0
    turnaround: int = 0
    waiting: int = 0

def calculate(process: Process, current: int):
    start = max(current, process.arrival)
    process.completion = start + process.burst
    process.turnaround = (process.completion - process.arrival)
    process.waiting = (process.turnaround - process.burst)
    return process.completion, start

def fcfs(items):
    processes = sorted(deepcopy(items), key=lambda p: (p.arrival, p.pid))
    current = 0
    timeline = []
    for process in processes:
        if current < process.arrival:
            timeline.append(("IDLE", current, process.arrival))
            current = process.arrival
        current, start = calculate(process, current)
        timeline.append((process.pid, start, current))
    return processes, timeline

def sjf(items):
    processes = deepcopy(items)
    remaining = processes[:]
    completed = []
    timeline = []
    current = 0
    while remaining:
        ready = [process for process in remaining if process.arrival <= current]
        if not ready:
            next_arrival = min(process.arrival for process in remaining)
            timeline.append(("IDLE", current, next_arrival))
            current = next_arrival
            continue
        process = min(ready, key=lambda p: (p.burst, p.arrival, p.pid))
        current, start = calculate(process, current)
        timeline.append((process.pid, start, current))
        completed.append(process)
        remaining.remove(process)
    return completed, timeline

def print_result(name, processes, timeline):
    print(f"\n{name}")
    print("PID AT BT CT TAT WT")
    for process in processes:
        print(process.pid, process.arrival, process.burst, process.completion, process.turnaround, process.waiting)
    print("Timeline:", timeline)

data = [
    Process("P1", 0, 7),
    Process("P2", 2, 4),
    Process("P3", 4, 1),
    Process("P4", 5, 4)
]

fcfs_result, fcfs_timeline = fcfs(data)
sjf_result, sjf_timeline = sjf(data)
print_result("FCFS", fcfs_result, fcfs_timeline)
print_result("SJF", sjf_result, sjf_timeline)