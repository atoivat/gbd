"""Classes representando as duas tabelas utilizadas no exercício (Aluno e Curso), com funcionalidades pra gravar e ler registros do disco."""
from dataclasses import dataclass
from typing import Literal


@dataclass
class Registro:
    """Objeto Python que poderá ser facilmente convertido em um registro a ser salvo no banco (arquivo)

    É esperado que as classes que herdem de `Registro` definam seus atributos e o tamanho dos mesmos, seguinto o fomato:
        - <nome do atributo> -> guardará o valor do campo em si
        _ _meta_<nome do atributo> -> guarda metadados (no caso, o tamanho do atributo em bytes a ser utilizado no processo de conversão).
    """

    def to_registry(self) -> bytes:
        """
        Converte o objeto python para o formato de registro a ser salvo no banco (arquivo)
        """
        resulting_bytes = b""

        for attr_name in self.__dict__.keys():
            if attr_name[0] == "_":
                # Ignora atributos "privados"
                continue
            attr_value = getattr(self, attr_name)
            attr_size = getattr(self, f"_meta_{attr_name}")

            if type(attr_value) == int:
                resulting_bytes += attr_value.to_bytes(
                    attr_size,
                    "big",
                    signed=True,
                )
            else:
                # Deixa a string sempre com um tamanho fixo
                attr_str_fixed_len = attr_value.ljust(attr_size, " ")[:attr_size]
                resulting_bytes += attr_str_fixed_len.encode()

        return resulting_bytes

    @classmethod
    def from_registry(cls, readed_bytes: bytes):
        """Converte bytes em uma instância da classe em questão."""
        read_attributes = []

        current_offset = 0
        for attr_name in cls.__dict__.keys():
            if attr_name[:6] != "_meta_":
                # Ignora atributos que não sejam metadados
                continue

            real_attr_name = attr_name[6:]
            field_size = getattr(cls, attr_name)
            real_attr_type = cls.__annotations__[real_attr_name]

            readed_attr = readed_bytes[current_offset : (current_offset + field_size)]
            # print(
            #     real_attr_name,
            #     real_attr_type,
            #     field_size,
            # )
            current_offset += field_size

            if real_attr_type == int:
                read_value = int.from_bytes(readed_attr, "big", signed=True)
            else:
                read_value = readed_attr.decode()
            # print("\t", read_value)
            read_attributes.append(read_value)

        return cls(*read_attributes)

    @classmethod
    def size(cls) -> int:
        """Retorna o tamanho em bytes daquele registro no arquivo do banco."""
        total_size = 0
        for attr_name in cls.__dict__.keys():
            if attr_name[:6] != "_meta_":
                # Ignora atributos que não sejam metadados
                continue

            total_size += getattr(cls, attr_name)
        return total_size


@dataclass
class Aluno(Registro):
    seq_aluno: int
    codigo_curso: str
    nome_aluno: str

    _meta_seq_aluno: Literal[4] = 4
    _meta_codigo_curso: Literal[3] = 3
    _meta_nome_aluno: Literal[33] = 33


@dataclass
class Curso(Registro):
    seq_curso: int
    codigo_curso: str
    nome_curso: str

    _meta_seq_curso: Literal[4] = 4
    _meta_codigo_curso: Literal[3] = 3
    _meta_nome_curso: Literal[17] = 17


def main():
    a = Aluno(8, "BCC", "Otávio Leite")
    print(a)
    a_bytes = a.to_registry()
    print(a_bytes)
    a_reconverted = Aluno.from_registry(a_bytes)
    print(a_reconverted)

    c = Curso(1, "BCC", "C. da Computacao")
    c_bytes = c.to_registry()
    print(c_bytes)
    c_reconverted = Curso.from_registry(c_bytes)
    print(c_reconverted)


if __name__ == "__main__":
    main()
