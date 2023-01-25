"""Gera arquivos a serem utilizados nos algoritmos, um pra cada tabela."""
import random
import string
from pprint import pprint

from database_entities import Aluno, Curso, Registro


def write_registros(registros: list[Registro], file_path: str = "registros.bin"):
    with open(file_path, "wb") as file:
        for registro in registros:
            file.write(registro.to_registry())


def read_registros(type_cls, file_path) -> list:
    registros = []
    with open(file_path, "r+b") as file:
        while len(data_read := file.read(type_cls.size())) > 0:
            registros.append(type_cls.from_registry(data_read))
    return registros


def generate_cursos(size: int) -> list[Curso]:
    """Gera cursos aleatórios"""
    cursos = []
    for n in range(size):
        rand_string = "".join(random.choice(string.ascii_letters) for i in range(17))
        cursos.append(
            Curso(
                seq_curso=n + 1,
                codigo_curso=rand_string[:3],
                nome_curso=rand_string,
            )
        )

    return cursos


def generate_alunos(size: int, cursos: list[Curso]):
    """Gera alunos aleatórios, matriculados aleatoriamente em algum curso"""
    alunos = []
    for n in range(size):
        rand_string = "".join(random.choice(string.ascii_letters) for i in range(33))
        alunos.append(
            Aluno(
                seq_aluno=n + 1,
                codigo_curso=random.choice(cursos).codigo_curso,
                nome_aluno=rand_string,
            )
        )
    return alunos


def main():
    cursos = generate_cursos(2)
    alunos = generate_alunos(3, cursos)

    # Embaralha a ordem dos cursos
    random.shuffle(cursos)
    pprint(cursos)

    # Embaralha a ordem dos alunos
    random.shuffle(alunos)
    pprint(alunos)

    write_registros(alunos, "alunos.bin")
    write_registros(cursos, "cursos.bin")

    print("==" * 100)

    pprint(read_registros(Aluno, "alunos.bin"))
    pprint(read_registros(Curso, "cursos.bin"))


if __name__ == "__main__":
    main()
