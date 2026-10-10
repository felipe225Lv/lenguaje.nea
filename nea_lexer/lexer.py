
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

# Tipos de datos propuestos para .nea
TIPOS = {
    "numero",
    "decimal",
    "texto",
    "booleano",
}

SIMBOLOS_DOBLES = {"==", "!=", ">=", "<="}

SIMBOLOS = {
    ";", "(", ")", "{", "}", "[", "]",
    ",", ".", ":", "+", "-", "*", "/",
    "=", "<", ">", "!",
}


def tokenizar(texto):
    """Devuelve tuplas (tipo, lexema, linea, columna)."""
    tokens = []
    posicion = 0
    linea = 1
    columna = 1

    while posicion < len(texto):
        caracter = texto[posicion]

        # Saltos de línea
        if caracter == "\n":
            posicion += 1
            linea += 1
            columna = 1
            continue

        # Espacios y tabulaciones
        if caracter.isspace():
            posicion += 1
            columna += 1
            continue

        # Tarea 6: comentarios // hasta el final de la línea
        if texto.startswith("//", posicion):
            while posicion < len(texto) and texto[posicion] != "\n":
                posicion += 1
                columna += 1
            # No consumimos el salto de línea: lo procesa el siguiente ciclo.
            continue

        # Números enteros y decimales
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

            tokens.append((
                "NUMERO",
                texto[inicio:posicion],
                linea,
                columna_inicio,
            ))
            continue

        # Cadenas entre comillas dobles
        if caracter == '"':
            columna_inicio = columna
            posicion += 1
            columna += 1
            inicio = posicion

            while posicion < len(texto) and texto[posicion] not in {'"', "\n"}:
                posicion += 1
                columna += 1

            if posicion >= len(texto) or texto[posicion] != '"':
                raise ValueError(
                    f"Cadena sin cerrar en linea {linea}, "
                    f"columna {columna_inicio}"
                )

            cadena = texto[inicio:posicion]
            tokens.append(("CADENA", cadena, linea, columna_inicio))

            posicion += 1
            columna += 1
            continue

        # Identificadores, tipos y palabras reservadas
        if caracter.isalpha() or caracter == "_":
            inicio = posicion
            columna_inicio = columna

            while (
                posicion < len(texto)
                and (
                    texto[posicion].isalnum()
                    or texto[posicion] == "_"
                )
            ):
                posicion += 1
                columna += 1

            palabra = texto[inicio:posicion]

            if palabra in TIPOS:
                tipo = "TIPO"
            elif palabra in PALABRAS_RESERVADAS:
                tipo = "PALABRA_RESERVADA"
            else:
                tipo = "IDENTIFICADOR"

            tokens.append((tipo, palabra, linea, columna_inicio))
            continue

        # Tarea 5: revisar primero símbolos de dos caracteres
        posible_simbolo = texto[posicion:posicion + 2]

        if posible_simbolo in SIMBOLOS_DOBLES:
            tokens.append(("SIMBOLO", posible_simbolo, linea, columna))
            posicion += 2
            columna += 2
            continue

        # Símbolos de un carácter: incluye = y ;
        if caracter in SIMBOLOS:
            tokens.append(("SIMBOLO", caracter, linea, columna))
            posicion += 1
            columna += 1
            continue

        # Tarea 6.1: error léxico con posición exacta
        raise ValueError(
            f"Caracter no reconocido {caracter!r} "
            f"en linea {linea}, columna {columna}"
        )

    return tokens