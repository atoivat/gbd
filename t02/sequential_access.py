import time
import os


def sequential_access(file, registers_per_page: int):
    """
    Receives the file and the number of registers per page.
    Returns:
        - Amount of valid registers
        - Amount of read pages
        - Processing time
    """
    initial_time = time.time()
    valid_registers_count = 0
    read_pages_count = 0

    length_loaded = registers_per_page*50
    file_size = os.path.getsize(file)

    with open(file, "r+b") as f:

        while file_size > 0:
            can_load_page = (file_size // length_loaded) > 0

            if can_load_page:
                page = f.read(length_loaded)
                file_size -= length_loaded
            else:
                page = f.read(file_size)
                file_size -= file_size

            valid_registers_on_page = process_page(page)

            valid_registers_count += valid_registers_on_page
            read_pages_count += 1\

    f.close()

    total_time = time.time() - initial_time

    return valid_registers_count, read_pages_count, total_time


def process_page(page_records: bytes) -> int:
    page_size = len(page_records)
    registers_on_page = page_size // 50

    valid_registers_count = 0
    for register_idx in range(registers_on_page):
        register = page_records[register_idx*50: (register_idx+1)*50]
        nseq = int.from_bytes(register[:4], 'big', signed=True)
        if nseq >= 0:
            valid_registers_count += 1

    return valid_registers_count
