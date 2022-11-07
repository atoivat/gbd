import os
import random
import time


def random_sweep(file_path: str, registers_to_read: int):

    initial_time = time.time()
    valid_registers = 0
    invalid_registers = 0

    file_size = os.path.getsize(file_path)
    total_reg_num = file_size // 50

    while registers_to_read > 0:
        random_reg = random.randint(0, total_reg_num - 1)

        with open(file_path, "r+b") as f:
            f.seek(random_reg * 50)

            read = f.read(4)
            nseq = int.from_bytes(read, "big", signed=True)

            if nseq < 0:
                invalid_registers += 1
            else:
                valid_registers += 1
        f.close()

        registers_to_read -= 1

    total_time = time.time() - initial_time

    return total_time, valid_registers, invalid_registers
