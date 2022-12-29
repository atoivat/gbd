"""Funções úteis"""
import os
import random
import string


def create_heap_file(file_path: str, nro_de_registros: int) -> bool:
    """
    Create an file with [nro_de_registros] of registers, in each one
    the 4 first bytes goes to NSEQ(int) which is ordered,
    and the last 46 bytes are for data TEXT[char] with is random too.
    """

    try:
        with open(file_path, "wb") as file:
            for i in range(nro_de_registros):
                # write NSEQ
                file.write(i.to_bytes(4, "big", signed=True))

                # write random DATA
                rand_string = "".join(
                    random.choice(string.ascii_letters) for _ in range(46)
                )
                # print(f'{i} - {rand_string} ')

                if i % 20000 == 0:
                    print("...", i)

                file.write(rand_string.encode())

            file.close()

            # check file size
            print("File Size= ", os.path.getsize(file_path))
            return True
    except:
        return False
