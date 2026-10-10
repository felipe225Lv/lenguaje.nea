from .lexer import tokenizar


def main():
    print(tokenizar("20;"))
    print(tokenizar("5;\n12;"))
    print(tokenizar("edad nota"))


if __name__ == "__main__":
    main()
