INITIAL_BUCKET_NO = 4
BUCKET_SIZE = 4


def hash_f(hi: int, key: int):
    """Aplica a função de hash, de acordo com o tamanho atual do diretório."""
    mod_op = 2**hi
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
            empty_buckets_str = " " * 50 * BUCKET_SIZE * INITIAL_BUCKET_NO
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


h = LinearHash("./hash.txt", "./overflow.txt", "data.txt")
print(h.create_files())
