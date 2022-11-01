def main():
    nro_de_registros = int(input("Número de registros: "))
    create_heap_file(nro_de_registros)


def create_heap_file(nro_de_registros: int):
    # Inteiros
    # testing_file.write((137).to_bytes(4, 'big', signed=True))
    # int.from_bytes(b'\x00\x00\x00\x89', 'big', signed=True)

    # Strings
    # testing_file.write("teste".encode())
    # b'teste'.decode()
    pass


def read_random(file, nseq: int):
    pass


def isrt_at_end(file):
    pass


def update_random(file, nseq: int, novo_text: str):
    pass


def delete_random(file, nseq: int):
    pass


if __name__ == "__main__":
    main()
