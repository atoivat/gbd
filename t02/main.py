import random
import string
import os


file_path = './register_file.txt'


def main():
    nro_de_registros = int(input("Número de registros: "))

    if not create_heap_file(nro_de_registros):
        print("Erro na criaçao de arquivo...")
        exit()

    rand_acess = random.randint(0, nro_de_registros-1)
    if not read_random(file_path, rand_acess):
        print("Erro na leitura aleatoria de arquivo...")
        exit()

    if not isrt_at_end(file_path):
        print("Erro na insercao de registro ...")
        exit()
    nro_de_registros += 1

    print_file(nro_de_registros)

    rand_string = ''.join(random.choice(
        string.ascii_letters) for i in range(46))

    rand_update = random.randint(0, nro_de_registros-1)
    if not update_random(file_path, rand_update, rand_string):
        print("Erro no update do registro ...")
        exit()

    print_file(nro_de_registros)

    rand_delete = random.randint(0, nro_de_registros-1)
    if not delete_random(file_path, rand_delete):
        print("Erro na deleção de registro ...")
        exit()
    print_file(nro_de_registros)


def print_file(nro_de_registros: int):

    try:
        with open(file_path, 'r+b') as file:
            for _ in range(nro_de_registros):
                nseq_part = file.read(4)
                nseq_part = int.from_bytes(
                    nseq_part, 'big', signed=True)

                data_part = file.read(46)
                register_searched = f'{nseq_part} - {data_part.decode()}'
                print('register  = ', register_searched)

            file.close()
    except:
        print("Erro na leitura do arquivo")


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

                # write random DATA
                rand_string = ''.join(random.choice(
                    string.ascii_letters) for i in range(46))
                print(f'{i} - {rand_string} ')
                file.write(rand_string.encode())

            file.close()

            # check file size
            print('File Size= ', os.path.getsize("./register_file.txt"))
            return True
    except:
        return False


def read_random(file_path: str, nseq: int):
    '''Given a [file] access the register in the [nseq] asked'''
    # [TODO] check nseq == -1  ?
    try:
        with open(file_path, 'r') as file:
            # Working the index arithmetic
            file.seek(nseq*50)

            nseq_part = file.read(4)
            nseq_part = int.from_bytes(nseq_part.encode(), 'big', signed=True)

            data_part = file.read(46)
            register_searched = f'{nseq_part} - {data_part}'
            print(
                f'Reading  Random at number = {nseq} ...\n... Register value = ', register_searched)

        file.close()
        return True

    except:
        return False


def isrt_at_end(file_path: str):
    '''Insert a value to the end of the file'''

    offset = os.path.getsize("./register_file.txt")
    nro_reg = offset//50

    try:
        with open(file_path, 'r+b') as file:

            file.seek(offset)

            file.write(nro_reg.to_bytes(4, 'big', signed=True))

            rand_string = ''.join(random.choice(
                string.ascii_letters) for i in range(46))
            print(f'Insert at the end ...\n... {nro_reg} - {rand_string}  ')
            file.write(rand_string.encode())

        file.close()
        return True

    except:
        return False


def update_random(file, nseq: int, new_text: str):
    '''Update Register at [nseq] index, with the new value [new_text]'''

    print(f'Update at {nseq}...')
    try:
        with open(file_path, 'r+b') as file:

            file.seek((nseq*50) + 4)
            file.write(new_text.encode())

        file.close()
        return True

    except:
        return False


def delete_random(file, nseq: int):

    print(f'Deleting index at {nseq}... ')
    try:
        with open(file_path, 'r+b') as file:

            file.seek(nseq*50)

            nseq_read = file.read(4)
            nseq_read = int.from_bytes(nseq_read, 'big', signed=True)

            file.seek(nseq*50)
            res = (nseq_read*(-1)).to_bytes(4, 'big', signed=True)
            file.write(res)

        file.close()
        return True

    except:
        return False


if __name__ == "__main__":
    main()
