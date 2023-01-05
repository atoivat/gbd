from io import SEEK_CUR, SEEK_END

INITIAL_BUCKET_NO = 4
BUCKET_SIZE = 4
REGISTER_SIZE = 50


def hash_f(hi: int, key: int):
    """Aplica a função de hash, de acordo com o tamanho atual do diretório."""
    mod_op = (2**hi) * INITIAL_BUCKET_NO
    return key % mod_op


class LinearHash:
    def __init__(
        self,
        hash_file_path: str,
        overflow_file_path: str,
        data_file_path: str | None,
    ) -> None:
        """Inicializa objeto com os caminhos dos arquivos."""
        self.hash_file_path = hash_file_path
        self.overflow_file_path = overflow_file_path
        self.data_file_path = data_file_path

    def __del__(self):
        """Desaloca recursos do objeto (fecha os arquivos abertos)"""
        self.hash_file.close()
        self.overflow_file.close()
        if self.data_file_path is not None:
            self.data_file.close()

    def load_files(self):
        """Carrega os arquivos para memória, dado seus caminhos."""
        self.hash_file = open(self.hash_file_path, "rb+")
        self.overflow_file = open(self.overflow_file_path, "rb+")
        self.data_file = None
        if self.data_file_path is not None:
            self.data_file = open(self.data_file_path, "rb+")

    def create_files(self) -> bool:
        """
        Cria os arquivos do hash, e já os carrega para memória, dado seus caminhos.
        Não cria novos arquivos se eles já existirem, apenas carrega eles pra memória.
        Retorna um booleano representando se houve ou não criação de novos arquivos.
        """
        try:
            self.load_files()
        except FileNotFoundError:
            # Arquivos ainda não existem, os cria
            self.hash_file = open(self.hash_file_path, "wb+")
            self.overflow_file = open(self.overflow_file_path, "wb+")
            self.data_file = None
            if self.data_file_path is not None:
                self.data_file = open(self.data_file_path, "wb+")

            # Inicializa ponteiros (level = 0, next = 0, current_bucket_no = INITIAL_BUCKET_NO)
            self.hash_file.write((0).to_bytes(4, "big", signed=True))
            self.hash_file.write((0).to_bytes(4, "big", signed=True))
            self.hash_file.write((INITIAL_BUCKET_NO).to_bytes(4, "big", signed=True))

            # cria os "INITIAL_BUCKET_NO" buckets
            empty_buckets_str = (
                " " * (REGISTER_SIZE * BUCKET_SIZE + 4) * INITIAL_BUCKET_NO
            )
            self.hash_file.write(empty_buckets_str.encode())

            self.hash_file.seek(0)

            return True
        # Arquivos já existem e foram carregados
        return False

    @property
    def level(self):
        """
        Retorna o nível atual do hash linear.
        Primeiro inteiro do 'hash_file' (4 bytes).
        Offset: 0
        """
        self.hash_file.seek(0)
        return int.from_bytes(self.hash_file.read(4), "big", signed=True)

    @level.setter
    def level(self, value: int):
        self.hash_file.seek(0)
        self.hash_file.write(value.to_bytes(4, "big", signed=True))

    @property
    def nxt(self):
        """
        Retorna o ponteiro 'NEXT' do hash linear.
        Segundo inteiro do 'hash_file' (4 bytes).
        Offset: 4 bytes
        """
        self.hash_file.seek(4)
        return int.from_bytes(self.hash_file.read(4), "big", signed=True)

    @nxt.setter
    def nxt(self, value: int):
        self.hash_file.seek(4)
        self.hash_file.write(value.to_bytes(4, "big", signed=True))

    @property
    def current_bucket_no(self):
        """
        Retorna o número de buckets atualmente no hash.
        Terceiro inteiro do 'hash_file' (4 bytes).
        Offset: 8 bytes
        """
        self.hash_file.seek(8)
        return int.from_bytes(self.hash_file.read(4), "big", signed=True)

    @current_bucket_no.setter
    def current_bucket_no(self, value: int):
        self.hash_file.seek(8)
        self.hash_file.write(value.to_bytes(4, "big", signed=True))

    def search_key(self, key: int) -> bytes:
        """
        Busca o registro no hash, a partir da chave.
        Retorna os bytes correspondentes à 'data entry'.
        """

        target_bucket = hash_f(self.level, key)

        if target_bucket < self.nxt:
            # Bucket alvo sofreu um split, necessario uma segunda funcao hash_f+1
            target_bucket = hash_f(self.level + 1, key)

        target_bucket_start = 12 + (REGISTER_SIZE * BUCKET_SIZE + 4) * target_bucket

        # Posiciona o #HEAD do arquivo no offset do bucket buscado
        self.hash_file.seek(target_bucket_start)

        searching_file = self.hash_file
        current_pos = 0

        while True:

            data_read = searching_file.read(4)

            if int.from_bytes(data_read, "big", signed=True) == key:
                # Achamos a chave
                r_nseq = int.from_bytes(data_read, "big", signed=True)
                r_text = searching_file.read(46)

                return (r_nseq, r_text.decode())
            else:

                current_pos += 1
                searching_file.seek(46, SEEK_CUR)

                # todos os slots estao preenchidos?
                if current_pos >= 4:
                    # Lida com página de overflow
                    pointer_data = searching_file.read(4)

                    # TODO: conferir esse caso
                    print(str(pointer_data.decode()))
                    if pointer_data.decode() == " " * 4:
                        return (-1, -1)

                    # TODO: conferir esse caso
                    elif pointer_data.decode() == str(key):

                        r_nseq = int(pointer_data.decode())
                        r_text = searching_file.read(46)
                        return (r_nseq, r_text)
                    else:
                        overflow_pointer = int.from_bytes(
                            pointer_data, "big", signed=True
                        )

                    # Move a busca para a página de overflow
                    searching_file = self.overflow_file
                    searching_file.seek(
                        (REGISTER_SIZE * BUCKET_SIZE + 4) * overflow_pointer
                    )
                    current_pos = 0

    def insert(self, nseq: int, text: str, check_split: bool = True):
        """Inserção de registro no hash."""

        # TODO: Conferir se nseq já existe no hash antes de inserir!!!

        target_bucket = hash_f(self.level, nseq)

        if target_bucket < self.nxt:
            # Bucket alvo sofreu um split, necessario uma segunda funcao hash_f+1
            target_bucket = hash_f(self.level + 1, nseq)

        # Busca posição vazia
        target_bucket_start = 12 + (REGISTER_SIZE * BUCKET_SIZE + 4) * target_bucket

        # Posiciona o #HEAD do arquivo no offset do bucket buscado
        self.hash_file.seek(target_bucket_start)

        searching_file = self.hash_file
        current_pos = 0
        overflow_pointer = None
        new_overflow = False

        while True:
            data_read = searching_file.read(4)

            if data_read.decode() == " " * 4:
                # Achou posição vazia
                searching_file.seek(-4, SEEK_CUR)
                break
            current_pos += 1
            searching_file.seek(46, SEEK_CUR)

            # todos os slots estao preenchidos?
            if current_pos >= 4:
                # Lida com página de overflow
                pointer_data = searching_file.read(4)

                if pointer_data.decode() == " " * 4:
                    # Página de overflow ainda não existe, deve criar
                    # Cria página de overflow
                    new_overflow = True

                    # Salva posição do searching_file referente ao ponteiro para
                    # o bucket que será criado
                    searching_file.seek(-4, SEEK_CUR)
                    bucket_pointer_offset = searching_file.tell()

                    # TODO: procurar um bucket vazio desde o começo do arquivo,
                    # olhando de 204 em 204 bytes, até um primeiro bucket vazio
                    # disponível
                    self.overflow_file.seek(0, SEEK_END)
                    new_overflow_pointer = self.overflow_file.tell()

                    empty_bucket_str = " " * (REGISTER_SIZE * BUCKET_SIZE + 4)
                    self.overflow_file.write(empty_bucket_str.encode())

                    # Escreve o ponteiro para a página criada
                    searching_file.seek(bucket_pointer_offset)
                    searching_file.write(
                        new_overflow_pointer.to_bytes(4, "big", signed=True)
                    )

                    overflow_pointer = new_overflow_pointer
                    if searching_file == self.overflow_file: 
                        break
                else:
                    overflow_pointer = int.from_bytes(pointer_data, "big", signed=True)

                # Move a busca para a página de overflow
                searching_file = self.overflow_file
                searching_file.seek(
                    (REGISTER_SIZE * BUCKET_SIZE + 4) * overflow_pointer
                )
                current_pos = 0

        # Insere na posição vazia
        searching_file.write(nseq.to_bytes(4, "big", signed=True))
        searching_file.write(text.encode())

        if new_overflow and check_split:
            # Provocar um split
            self.split()
        return new_overflow

    def split(self):
        # Cria bucket vazio no final do hash file
        self.hash_file.seek(0, SEEK_END)
        empty_bucket_str = " " * (REGISTER_SIZE * BUCKET_SIZE + 4)
        self.hash_file.write(empty_bucket_str.encode())

        # Para toda as chaves no arquivo principal ou de overflow
        # faremos o calculo da nova funcao hash_f+1
        # hash_f(self.level+1, key) e assim distribuindo as chaves nos devidos buckets
        nxt_bucket_start = 12 + (REGISTER_SIZE * BUCKET_SIZE + 4) * self.nxt

        # Lê todas as entradas no bucket e nas páginas de overflow correspondentes,
        # zerando cada uma delas e armazenando os registros lidos numa lista em memória.
        # Atenção para "limpar" as páginas de overflow

        # lista de registros lidos
        registers = []

        current_bucket = nxt_bucket_start
        current_file = self.hash_file
        # Loop
        while True:
            # Lê o bucket atual inteiro
            current_file.seek(current_bucket)

            # Guarda os registros na lista de registros
            for _ in range(BUCKET_SIZE):
                register_content = current_file.read(REGISTER_SIZE)

                # Confere se registro não está vazio
                if register_content[:5].decode() == " " * 4:
                    continue

                nseq = int.from_bytes(register_content[:4], "big", signed=True)
                text = register_content[4:].decode()
                registers.append((nseq, text))

            # limpa todas as entradas no bucket atual, menos o ponteiro de overflow
            current_file.seek(current_bucket)
            empty_regs_str = " " * (REGISTER_SIZE * BUCKET_SIZE)
            current_file.write(empty_regs_str.encode())

            # Confere ponteiro da página de overflow
            overflow_pointer = current_file.read(4)
            # Se tiver:
            if overflow_pointer.decode() != " " * 4:
                overflow_pointer_value = int.from_bytes(
                    overflow_pointer, "big", signed=True
                )

                # Limpa o ponteiro para a página de overflow
                current_file.seek(-4, SEEK_CUR)
                current_file.write("    ".encode())

                # o bucket atual vira a página de overflow
                current_file = self.overflow_file
                current_bucket = overflow_pointer_value
            else:
                break

        self.nxt += 1
        # Confere se deve zerar o nxt e aumentar o level
        # (depois de uma rodada completa de splits)
        if self.nxt >= ((2**self.level) * INITIAL_BUCKET_NO):
            self.nxt = 0
            self.level += 1

        # A partir da lista de registros em memória, distribui os elementos entre os buckets (usando o algoritmo de inserção sem "check_split")
        for nseq, text in registers:
            self.insert(nseq, text, check_split=False)

        self.current_bucket_no += 1
