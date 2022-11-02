import random
import string
import os


file_path = './register_file.txt'


def main():
    nro_de_registros = int(input("Número de registros: "))

    if not create_heap_file(nro_de_registros):
        print("Erro na criaçao de arquivo...")
        exit()

    rand_acess = random.randint(0, nro_de_registros)
    print('rand acess, ', rand_acess)
    read_random(file_path, rand_acess)


def create_heap_file(nro_de_registros: int) -> bool:
    '''
    Create an file with [nro_de_registros] of registers, in each one 
    the 4 first bytes goes to NSEQ(int) which is ordered,
    and the last 46 bytes are for data TEXT[char] with is random too.
    '''

    try:
        with open(file_path, 'wb') as file:
            for i in range(nro_de_registros):
                # write NSEQ
                file.write(i.to_bytes(4, 'big', signed=True))
                print(i)

                # write random DATA
                rand_string = ''.join(random.choice(
                    string.ascii_letters) for i in range(46))
                print(rand_string)
                file.write(rand_string.encode())

            file.close()

            # check file size
            print(os.path.getsize("./register_file.txt"))
    except:
        return False
    finally:
        return True


def read_random(file: str, nseq: int):
    '''Given a [file] access the register in the [nseq] asked'''

    with open(file, 'r') as file:

        # Workin the index arithmetic
        for _ in range(nseq):
            file.read(50)

        register_searched = file.read(50)
        # Error at the int part, is printing as an Ascii char
        print(register_searched)
    file.close()


def isrt_at_end(file):
    pass


def update_random(file, nseq: int, novo_text: str):
    pass


def delete_random(file, nseq: int):
    pass


if __name__ == "__main__":
    main()
