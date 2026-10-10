PALABRAS_RESERVADAS = {
    "aVerQuePasa",
    "armeUno",
    "conCalma",
    "deUna",
    "dejeEso",
    "devuelvame",
    "elPatron",
    "enEsteCaso",
    "esoQuedaAsi",
    "espereUnMomentico",
    "esteMan",
    "hagaUnaVuelta",
    "hablame",
    "heredaDe",
    "mandePues",
    "mientrasTinto",
    "niDeRiesgo",
    "niRiesgo",
    "oQue",
    "paraPues",
    "parche",
    "paseLoQuePase",
    "segunElCaso",
    "seArmoLaGorda",
    "siNadaDeEso",
    "siNoPues",
    "siNoSiPues",
    "siPues",
    "siSeEmputa",
    "sigaPues",
    "sinPalabras",
    "tireLaBomba",
    "traigame",
    "unaVariable",
    "yTambien",
    "yaEsta",
}


SIMBOLOS_DOBLES = {"==", "!=", ">=", "<="}


SIMBOLOS = {
    ";",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    ",",
    ".",
    ":",
    "+",
    "-",
    "*",
    "/",
    "=",
    "<",
    ">",
    "!",
}


def tokenizar(texto):
    """Convierte un texto fuente en una lista de tokens.

    El lexer recorre el texto de izquierda a derecha usando `posicion`.
    Al mismo tiempo lleva `linea` y `columna` para guardar el lugar exacto
    donde empieza cada token.

    Cada token se devuelve como una tupla:
        (tipo, texto_del_token, linea, columna)
    """
    tokens = []
    posicion = 0
    linea = 1
    columna = 1

    while posicion < len(texto):
        caracter = texto[posicion]

        # El salto de linea cambia de renglon y reinicia la columna.
        if caracter == "\n":
            posicion += 1
            linea += 1
            columna = 1
            continue

        # Los espacios y tabulaciones separan tokens, pero no se guardan.
        if caracter.isspace():
            posicion += 1
            columna += 1
            continue

        # Un numero empieza con un digito y puede tener parte decimal.
        if caracter.isdigit():
            inicio = posicion
            columna_inicio = columna

            while posicion < len(texto) and texto[posicion].isdigit():
                posicion += 1
                columna += 1

            if (
                posicion + 1 < len(texto)
                and texto[posicion] == "."
                and texto[posicion + 1].isdigit()
            ):
                posicion += 1
                columna += 1

                while posicion < len(texto) and texto[posicion].isdigit():
                    posicion += 1
                    columna += 1

            numero = texto[inicio:posicion]
            tokens.append(("NUMERO", numero, linea, columna_inicio))
            continue

        # Una palabra empieza con letra y luego acepta letras, digitos o "_".
        # Si coincide con la tabla del lenguaje, es palabra reservada.
        if caracter.isalpha():
            inicio = posicion
            columna_inicio = columna

            while (
                posicion < len(texto)
                and (texto[posicion].isalpha() or texto[posicion].isdigit() or texto[posicion] == "_")
            ):
                posicion += 1
                columna += 1

            palabra = texto[inicio:posicion]
            tipo = "PALABRA_RESERVADA" if palabra in PALABRAS_RESERVADAS else "IDENTIFICADOR"
            tokens.append((tipo, palabra, linea, columna_inicio))
            continue

        # Los operadores como >= o == deben revisarse antes que > o =.
        posible_simbolo_doble = texto[posicion:posicion + 2]
        if posible_simbolo_doble in SIMBOLOS_DOBLES:
            tokens.append(("SIMBOLO", posible_simbolo_doble, linea, columna))
            posicion += 2
            columna += 2
            continue

        # Simbolos de un solo caracter: ;, (, ), +, -, etc.
        if caracter in SIMBOLOS:
            tokens.append(("SIMBOLO", caracter, linea, columna))
            posicion += 1
            columna += 1
            continue

        # Si no pertenece a ninguna regla, el lexer no sabe clasificarlo.
        raise ValueError(f"Caracter no reconocido {caracter!r} en linea {linea}, columna {columna}")

    return tokens
