"""
Lab 3 - Q2: Paging and segmentation.

Covers:
  * paging - a logical address is split into a page number and an offset,
    the page number is looked up in the page table and the physical address
    is rebuilt as frame * page_size + offset;
  * segmentation - a logical address is a (segment, offset) pair, the
    segment table holds a base/limit pair and the reference is valid only
    while the offset stays below the limit.

Run with:  python3 src/paging_segmentation.py
"""


def paging_translate(page_size, page_table, logical):
    """Translate a logical address through the page table.

    Returns (physical address, page number, offset). The physical address
    is None when the page is not mapped.
    """
    if page_size <= 0:
        raise ValueError("Page size must be positive")
    if logical < 0:
        raise ValueError("Logical address cannot be negative")

    page = logical // page_size
    offset = logical % page_size

    if page >= len(page_table):
        return None, page, offset

    frame = page_table[page]
    if frame is None or frame < 0:
        return None, page, offset

    physical = frame * page_size + offset
    return physical, page, offset


def segment_translate(segment_table, segment, offset):
    """Translate a (segment, offset) pair through the segment table.

    Returns the physical address, or None when the offset violates the
    limit of the segment.
    """
    if segment < 0 or offset < 0:
        raise ValueError("Segment and offset must be non-negative")
    if segment >= len(segment_table):
        return None

    base, limit = segment_table[segment]
    if offset >= limit:
        return None
    return base + offset


page_size = 1024
page_table = [5, 2, 8, None]
logical = 2500

physical, page, offset = paging_translate(page_size, page_table, logical)
print("Paging")
print("Page:", page, "Offset:", offset)
print("Physical:", physical if physical is not None else "Invalid page")

segment_table = [(1000, 400), (5000, 1200), (9000, 600)]
segment = 1
segment_offset = 350

segment_physical = segment_translate(segment_table, segment, segment_offset)
print("\nSegmentation")
print(
    "Physical:",
    segment_physical
    if segment_physical is not None
    else "Invalid segment reference",
)
