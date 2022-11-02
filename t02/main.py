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
    print('rand acess = ', rand_acess)

    if not read_random(file_path, rand_acess):
        print("Erro na leitura aleatoria de arquivo...")
        exit()

    if not isrt_at_end(file_path, "aseaosekaoek", nro_de_registros):
        print("Erro na insercao de registro ...")
        exit()

    print('size= ', os.path.getsize("./register_file.txt"))

    nro_de_registros += 1

    print_file(nro_de_registros)

    # if not read_random(file_path, rand_acess):
    #     print("Erro na leitura aleatoria de arquivo...")


def print_file(nro_de_registros: int):

    try:
        with open(file_path, 'r+') as file:
            for _ in range(nro_de_registros):
                nseq_part = file.read(4)
                nseq_part = int.from_bytes(
                    nseq_part.encode(), 'big', signed=True)

                data_part = file.read(46)
                register_searched = f'{nseq_part} - {data_part}'
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
            print(os.path.getsize("./register_file.txt"))
            return True
    except:
        return False


def read_random(file_path: str):
    '''Given a [file] access the register in the [nseq] asked'''
    offset = os.path.getsize("./register_file.txt")
    try:
        with open(file_path, 'r') as file:
            # Working the index arithmetic
            file.seek(offset)

            nseq_part = file.read(4)
            nseq_part = int.from_bytes(nseq_part.encode(), 'big', signed=True)

            data_part = file.read(46)
            register_searched = f'{nseq_part} - {data_part}'
            print('rand acess register val = ', register_searched)

        file.close()
        return True

    except:
        return False


def isrt_at_end(file_path: str, data: str, nro_reg: int):
    '''TODO: limit the number of bytes in [data]'''
    try:
        with open(file_path, 'r+b') as file:

            file.seek(nro_reg*50)
            print("where= ", file.tell())

            file.write(nro_reg.to_bytes(4, 'big', signed=True))
            file.write(data.encode())
            print(f'{nro_reg} - {data}')

        file.close()
        return True

    except:
        return False


def update_random(file, nseq: int, novo_text: str):
    pass


def delete_random(file, nseq: int):
    pass


if __name__ == "__main__":
    main()
