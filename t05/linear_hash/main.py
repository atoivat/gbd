"""IMPLEMENTAÇÃO DE ÍNDICES BASEADOS EM ÁRVORE B+ OU HASH DINÂMICO"""
import os

from linear_hash import LinearHash


def main():
    """Main"""

    h = LinearHash("./hash.txt", "./overflow.txt", "data.txt")
    print(h.create_files())

    h.insert(0, "zero")
    print(h.search_key(0))

    h.insert(4, "quatro")
    print(h.search_key(4))

    h.insert(8, "oito")
    print(h.search_key(8))

    h.insert(12, "doze")
    print(h.search_key(12))
    print(h.search_key(16))

    for i in range(0, 9):
        h.insert(3 + 4 * i, f"numero{3 + 4 * i}")

    # h.insert(16, "dezesseis")
    print(h.search_key(19))
    print(h.search_key(35))
    print(h.search_key(24))
    print(h.search_key(8))
    print(h.search_key(12))
    print(h.search_key(16))
    print(h.search_key(18))

    print(h.delete(8))
    print(h.search_key(8))
    print(h.insert(8, "oito"))
    print(h.insert(16, "dezesseis"))

    print(h.search_key(8))
    print(h.delete(8))

    print(h.insert(8, "oito"))

    print(h.insert(39, "trintanove"))

    print(h.delete(35))

    print(h.insert(43, "quarentatres"))

    print(h.delete(35))


if __name__ == "__main__":
    main()
