"""
Lab 3 - Q1: Swapping and address translation.

Covers:
  * dynamic memory allocation with the first-fit, best-fit and worst-fit
    strategies (the classic block splitting problem);
  * relocation through the base/limit register pair (base - limit
    addressing): a logical address is translated into a physical address
    only when it stays below the limit.

Run with:  python3 src/swapping_address_translation.py
"""

from copy import deepcopy


def validate_positive(values, label):
    """Every block and process size must be a positive number."""
    if not values:
        raise ValueError(f"{label} cannot be empty")
    if any(value <= 0 for value in values):
        raise ValueError(f"All {label} values must be positive")


def allocate(blocks, processes, method):
    """Allocate every process into a free block.

    method: "first" (first fit), "best" (best fit) or "worst" (worst fit).
    Returns the block index chosen for every process (-1 when the process
    does not fit anywhere) and the size of every block after the allocation.
    """
    validate_positive(blocks, "block")
    validate_positive(processes, "process")

    remaining = deepcopy(blocks)
    result = [-1] * len(processes)

    for process_index, process_size in enumerate(processes):
        candidates = [
            i for i, size in enumerate(remaining) if size >= process_size
        ]
        if not candidates:
            continue

        if method == "first":
            chosen = candidates[0]
        elif method == "best":
            chosen = min(candidates, key=lambda i: remaining[i])
        elif method == "worst":
            chosen = max(candidates, key=lambda i: remaining[i])
        else:
            raise ValueError("Unknown allocation method")

        result[process_index] = chosen
        remaining[chosen] -= process_size

    return result, remaining


def translate(base, limit, logical):
    """Translate a logical address into a physical address.

    None is returned when the logical address is outside the limit, i.e.
    when the reference does not belong to the process.
    """
    if base < 0 or limit <= 0 or logical < 0:
        raise ValueError(
            "Base and logical address must be non-negative; limit must be positive"
        )
    if logical >= limit:
        return None
    return base + logical


def print_allocation(name, blocks, processes, allocation, remaining):
    """Print the allocation table of one strategy."""
    print(f"\n{name}")
    print("Process Size Block")
    for i, size in enumerate(processes):
        block = allocation[i]
        label = "Not allocated" if block == -1 else f"B{block + 1}"
        print(f"P{i + 1:<7} {size:<4} {label}")
    print("Original blocks:", blocks)
    print("Remaining blocks:", remaining)


blocks = [100, 500, 200, 300, 600]
processes = [212, 417, 112, 426]

for method in ["first", "worst"]:
    allocation, remaining = allocate(blocks, processes, method)
    print_allocation(
        method.title() + " Fit", blocks, processes, allocation, remaining
    )

base = 1000
limit = 400
logical = 250
physical = translate(base, limit, logical)

print("\nAddress translation")
if physical is None:
    print("Invalid logical address")
else:
    print(f"Physical address = {physical}")
