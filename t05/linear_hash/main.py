"""IMPLEMENTAÇÃO DE ÍNDICES BASEADOS EM ÁRVORE B+ OU HASH DINÂMICO"""
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

    h.insert(16, "dezesseis")
    print(h.search_key(0))
    print(h.search_key(4))
    print(h.search_key(8))
    print(h.search_key(12))
    print(h.search_key(16))
    print(h.search_key(18))


if __name__ == "__main__":
    main()
