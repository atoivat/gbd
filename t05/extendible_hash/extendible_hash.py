from common import *


def hash_f(hi: int, key: int):
    """Aplica a função de hash, de acordo com o tamanho atual do diretório."""
    mod_op = 2**hi
    return key % mod_op


def create_hash_index_file(max_bucket_no: int, bucket_size: int, data_entry_size: int):
    """Cria arquivo de índice utilizando Hash Extensível"""


def create_directory() -> Directory:
    return Directory()


def insertKey(directory: Directory, data_entry: int) -> bool:
    """Insere o [data_entry] no Bucket ID certo, se for preciso irá fazer o split"""
    bucket_id = hash_f(directory.global_depth, data_entry)

    print(f"Bucket ID {bucket_id}")

    if len(directory.buckets[bucket_id].slots) == 4:
        # Will Split(SMITH)
        pass
    else:
        return True


def splitBucket(directory: Directory, data_entry: int, bucket_id: int):
    local_depth = directory.buckets[bucket_id].local_depth

    if local_depth < directory.global_depth:
        pass
        # split bucket

        # Precisa ver quantos buckets apontam para o q vai fazer split
        # Eh possivel usar a formula 2**(directory.global_depth - local_depth)
        # Se for dois belezura, um sera o bucket velho e o outro o novo
        # se for > 2 Ferrou! porq vai ter q tratar os outros ponteiros

    elif local_depth == directory.global_depth:
        pass
        # cry...

        # Dobra o diretorio
        # Mexer os ponteiros para apontar para os bucket certos
        # Tem como saber os valores dos buckets é só somar 2**global
        # (antes de incrementar o valor da prof global )


def removeKey(directory: Directory, data_entry: int) -> bool:
    """Remove o [data_entry] no Bucket ID certo, se for preciso irá fazer o merge"""
    bucket_id = hash_f(directory.global_depth, data_entry)

    print(f"Bucket ID {bucket_id}")

    # Se removido causara um merge
    if (len(directory.buckets[bucket_id].slots) - 1) == 0:
        # Verificar se eh um simples merge

        # se for entao, somente fara o bucket atual apontar para
        # if directory.buckets[bucket_id].bucked_id - 2**(directory.buckets[bucket_id].local_depth - 1) > 0
        # bucket = directory.buckets[bucket_id].bucked_id - 2**(directory.buckets[bucket_id].local_depth - 1)
        # else
        # bucket = directory.buckets[bucket_id].bucked_id + 2**(directory.buckets[bucket_id].local_depth - 1)

        # Se todos os bucket irao ficar com profundidade (global - 1)  apos o merge
        # Ferrou!
        # ira diminuir o diretorio por 2

        pass
    else:
        directory.buckets[bucket_id].slots.remove(data_entry)
        return True


def searchKey(directory: Directory, data_entry: int) -> bool:
    bucket_id = hash_f(directory.global_depth, data_entry)

    try:
        indx_value = directory.buckets[bucket_id].slots.index(data_entry)
        print(
            f"Valor {data_entry}, localizado no bucket {bucket_id} no índice {indx_value}"
        )
        return True
    except ValueError:
        return False


def Menu():
    while True:
        try:
            print("----- Menu -----")
            print("0 - Create Dir(NECESSARIO SER O PRIMEIRO PASSO)")
            print("1 - Insert in Dir")
            print("2 - Remove in Dir")
            print("3 - Search in Dir")
            print("4 - Print Current Dir")

            inp = int(input())

            if inp == 0:
                main_directory = create_directory()
            elif inp == 1:
                data_entry = int(input("Qual o valor? "))
                hasInserted = insertKey(main_directory, data_entry)
                if not hasInserted:
                    print(f"Error while inserting value {data_entry}")
                pass
            elif inp == 2:
                data_entry = int(input("Qual o valor? "))
                hasRemoved = removeKey(main_directory, data_entry)
                if not hasRemoved:
                    print(f"Error while removing value {data_entry}")
                pass
            elif inp == 3:
                data_entry = int(input("Qual o valor? "))
                hasValue = searchKey(main_directory, data_entry)
                if not hasValue:
                    print("Valor não existente...")
                pass
            elif inp == 4:
                main_directory.toString()
        except EOFError:
            break
