import os
import random
import string

from heap_file_functions import input_main
from random_access import random_sweep
from sequential_access import sequential_access

file_path = "./register_file.txt"


def main_a():
    input_main(file_path)


def main_b():
    """Implementação da questão 1.B - Experimentos com varredura sequencial."""
    # ask user input
    registers_per_page = int(input("Tamanho da página: "))

    # call function [sequential_access]
    register_count, readed_pages, proc_time = sequential_access(
        file_path, registers_per_page
    )

    # print results
    print(
        "Quantidade de registros validos:",
        register_count,
        "\nNumero de paginas lidas:",
        readed_pages,
        "\nTempo de processamento:",
        proc_time,
    )


def main_c():
    """Implementação da questão 1.C - Experimentos de acesso aleatório."""
    register_amount = int(input("Quantidade de registros: "))

    total_time, valid_registers, invalid_registers = random_sweep(
        file_path, register_amount
    )

    print(
        "Tempo de processamento:",
        total_time,
        "\nQuantidade de registros validos lidos:",
        valid_registers,
        "\nQuantidade de registros invalidos lidos:",
        invalid_registers,
    )


if __name__ == "__main__":
    main_a()
