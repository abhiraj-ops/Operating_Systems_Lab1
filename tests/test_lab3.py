"""
Tests for the Lab 3 programs.

The programs are plain scripts, so they are loaded straight from their
`src/` folder and their functions are checked against the expected results.
"""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

PROGRAMS = {
    "swapping": "Lab3/Q1_Swapping_Address_Translation/src/swapping_address_translation.py",
    "paging": "Lab3/Q2_Paging_Segmentation/src/paging_segmentation.py",
    "replacement": "Lab3/Q3_FIFO_LRU/src/fifo_lru.py",
    "devices": "Lab3/Q4_Device_Allocation/src/device_allocation.py",
    "disk": "Lab3/Q5_FCFS_SSTF_SCAN_c-SCAN/src/disk_scheduling.py",
}


def load(name):
    """Import one of the Lab 3 programs by its key in PROGRAMS."""
    path = REPO_ROOT / PROGRAMS[name]
    spec = importlib.util.spec_from_file_location(f"lab3_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def swapping():
    return load("swapping")


@pytest.fixture(scope="module")
def paging():
    return load("paging")


@pytest.fixture(scope="module")
def replacement():
    return load("replacement")


@pytest.fixture(scope="module")
def devices():
    return load("devices")


@pytest.fixture(scope="module")
def disk():
    return load("disk")


# --- Q1: swapping and address translation ----------------------------------
def test_first_fit_allocation(swapping):
    allocation, remaining = swapping.allocate([100, 500, 200, 300, 600], [212, 417, 112, 426], "first")
    assert allocation == [1, 4, 1, -1]
    assert remaining == [100, 176, 200, 300, 183]


def test_worst_fit_allocation(swapping):
    allocation, remaining = swapping.allocate([100, 500, 200, 300, 600], [212, 417, 112, 426], "worst")
    assert allocation == [4, 1, 4, -1]
    assert remaining == [100, 83, 200, 300, 276]


def test_best_fit_allocation(swapping):
    allocation, _ = swapping.allocate([100, 500, 200, 300, 600], [212, 417, 112, 426], "best")
    assert allocation[0] == 3  # 300 is the smallest block that fits 212


def test_allocation_rejects_invalid_input(swapping):
    with pytest.raises(ValueError):
        swapping.allocate([], [10], "first")
    with pytest.raises(ValueError):
        swapping.allocate([100], [0], "first")
    with pytest.raises(ValueError):
        swapping.allocate([100], [10], "unknown")


def test_address_translation(swapping):
    assert swapping.translate(1000, 400, 250) == 1250
    assert swapping.translate(1000, 400, 450) is None


# --- Q2: paging and segmentation --------------------------------------------
def test_paging_translation(paging):
    physical, page, offset = paging.paging_translate(1024, [5, 2, 8, None], 2500)
    assert (page, offset) == (2, 452)
    assert physical == 8 * 1024 + 452


def test_paging_rejects_unmapped_page(paging):
    physical, page, offset = paging.paging_translate(1024, [5, 2, 8, None], 3500)
    assert physical is None
    assert (page, offset) == (3, 428)


def test_paging_rejects_invalid_input(paging):
    with pytest.raises(ValueError):
        paging.paging_translate(0, [1], 10)
    with pytest.raises(ValueError):
        paging.paging_translate(1024, [1], -1)


def test_segment_translation(paging):
    table = [(1000, 400), (5000, 1200), (9000, 600)]
    assert paging.segment_translate(table, 1, 350) == 5350
    assert paging.segment_translate(table, 1, 1500) is None
    assert paging.segment_translate(table, 9, 10) is None


# --- Q3: page replacement ----------------------------------------------------
REFERENCE = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]


def test_fifo_counts(replacement):
    hits, faults, trace = replacement.fifo(REFERENCE, 3)
    assert (hits, faults) == (3, 10)
    assert len(trace) == len(REFERENCE)


def test_lru_counts(replacement):
    hits, faults, trace = replacement.lru(REFERENCE, 3)
    assert (hits, faults) == (4, 9)
    assert len(trace) == len(REFERENCE)


def test_optimal_is_never_worse(replacement):
    fifo_hits, _, _ = replacement.fifo(REFERENCE, 3)
    optimal_hits, _, _ = replacement.optimal(REFERENCE, 3)
    assert optimal_hits >= fifo_hits
    assert (optimal_hits, len(REFERENCE) - optimal_hits) == (6, 7)


def test_replacement_rejects_invalid_input(replacement):
    with pytest.raises(ValueError):
        replacement.fifo([], 3)
    with pytest.raises(ValueError):
        replacement.lru([1, 2], 0)


# --- Q4: device allocation ----------------------------------------------------
def test_dedicated_device_is_exclusive(devices):
    printer = devices.Device("Printer", "dedicated")
    assert printer.request("P1") == "P1 allocated Printer"
    assert printer.request("P2") == "P2 queued for Printer"
    assert printer.owner == "P1"


def test_release_hands_the_device_over(devices):
    printer = devices.Device("Printer", "dedicated")
    printer.request("P1")
    printer.request("P2")
    assert printer.release("P1") == "P1 released Printer; P2 is now owner"
    assert printer.owner == "P2"


def test_release_requires_ownership(devices):
    printer = devices.Device("Printer", "dedicated")
    printer.request("P1")
    assert printer.release("P9") == "P9 does not own Printer"


def test_shared_device_serves_in_order(devices):
    disk = devices.Device("SharedDisk", "shared")
    disk.request("P3")
    disk.request("P4")
    assert disk.service_next() == "SharedDisk served P3"
    assert disk.service_next() == "SharedDisk served P4"
    assert disk.service_next() == "No pending request for SharedDisk"


def test_virtual_device_queues_requests(devices):
    virtual = devices.Device("VirtualPrinter", "virtual")
    assert virtual.request("P5") == "P5 submitted request to VirtualPrinter"
    assert virtual.service_next() == "VirtualPrinter served P5"


def test_buffer_limits(devices):
    buffer = devices.Buffer(3)
    assert buffer.put("A") == "Inserted A"
    assert buffer.put("B") == "Inserted B"
    assert buffer.put("C") == "Inserted C"
    assert buffer.put("D") == "Buffer full"
    assert buffer.get() == "Removed A"
    assert buffer.get() == "Removed B"


def test_buffer_rejects_invalid_capacity(devices):
    with pytest.raises(ValueError):
        devices.Buffer(0)


# --- Q5: disk scheduling ------------------------------------------------------
REQUESTS = [98, 183, 37, 122, 14, 124, 65, 67]


def test_movement_counts_the_jumps(disk):
    assert disk.movement([53, 65, 67]) == 14


def test_fcfs_path_and_movement(disk):
    path = disk.fcfs(REQUESTS, 53)
    assert path[0] == 53
    assert disk.movement(path) == 640


def test_sstf_is_never_worse_than_fcfs(disk):
    fcfs_movement = disk.movement(disk.fcfs(REQUESTS, 53))
    sstf_movement = disk.movement(disk.sstf(REQUESTS, 53))
    assert sstf_movement <= fcfs_movement
    assert sstf_movement == 236


def test_scan_visits_the_end_of_the_disk(disk):
    path = disk.scan(REQUESTS, 53, 0, 199, "right")
    assert path[0] == 53
    assert 199 in path
    assert disk.movement(path) == 331


def test_cscan_returns_to_the_beginning(disk):
    path = disk.cscan(REQUESTS, 53, 0, 199)
    assert path[0] == 53
    assert 199 in path and 0 in path
    assert disk.movement(path) == 382


def test_disk_scheduling_rejects_out_of_range_input(disk):
    with pytest.raises(ValueError):
        disk.validate(REQUESTS, 500, 0, 199)  # head outside the disk
    with pytest.raises(ValueError):
        disk.validate([250], 53, 0, 199)  # request outside the disk


def test_swap_space_allocation(disk):
    swap = disk.SwapSpace(10)
    assert swap.allocate("P1", 4) is True
    assert swap.bitmap[:4] == [1, 1, 1, 1]
    assert swap.allocate("P2", 5) is True
    assert swap.allocate("P3", 3) is False  # only one block is left
    assert swap.release("P1") is True
    assert swap.bitmap[:4] == [0, 0, 0, 0]
    assert swap.release("P1") is False
