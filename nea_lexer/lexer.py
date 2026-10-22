
"""Analizador lexico del lenguaje .nea.

El lexer recorre el codigo fuente de izquierda a derecha y genera tuplas con
la forma (tipo, texto, linea, columna). Primero se presenta la guia de tareas
del parcial y despues el algoritmo en su orden real de ejecucion.
"""


# GUIA DE TAREAS EN EL ORDEN DEL ENUNCIADO
#
# Esta lista sigue el orden academico del parcial. Dentro de tokenizar, las
# comprobaciones se ordenan por prioridad lexica para reconocer correctamente
# comentarios, literales, palabras, operadores y simbolos.
# Tarea 1: guardar la columna donde empieza cada token.
# Tarea 2: contar lineas y reiniciar la columna despues de cada salto.
# Tarea 3: reconocer palabras usadas como nombres de variables.
# Tarea 4: distinguir tipos, palabras reservadas e identificadores.
# Tarea 5: reconocer el signo de asignacion y el fin de instruccion.
# Tarea 6: ignorar comentarios sin perder el conteo de lineas.
# Tarea 6.1: informar errores lexicos con linea y columna.
# Tarea 6.2: reconocer numeros decimales y cadenas de texto.
# Tarea 6.3: reconocer los operadores aritmeticos +, - y *.
# Tarea 7: demostrar el resultado mediante los casos del archivo de pruebas.


# CONFIGURACION DEL LENGUAJE
# Estas tablas se declaran antes del algoritmo porque se consultan durante
# la clasificacion de palabras, operadores y simbolos.

# Tipos y palabras reservadas del lenguaje.
# La palabra se lee completa antes de consultar estos conjuntos.
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

TIPOS = {
    "numero",
    "decimal",
    "texto",
    "booleano",
    "int",
    "double",
}

# Signo de asignacion, fin de instruccion y simbolos auxiliares.
# En .nea se usan = para asignar y ; para finalizar. El conjunto tambien
# incluye simbolos auxiliares del lenguaje y comparaciones de dos caracteres.
# Los simbolos mas largos siempre se comprueban antes que los simples.
SIMBOLOS_DOBLES = {"==", "!=", ">=", "<="}
SIMBOLOS = {
    ";", "(", ")", "{", "}", "[", "]",
    ",", ".", ":", "/",
    "=", "<", ">", "!",
}

# Operadores aritmeticos de un caracter.
OPERADORES = {"+", "-", "*"}


def tokenizar(texto):
    """Recorre el codigo fuente y devuelve (tipo, lexema, linea, columna).

    El orden de las comprobaciones es importante: primero se descartan
    separadores y comentarios; despues se leen los literales e identificadores;
    y al final se reconocen operadores y simbolos. Si ninguna regla acepta el
    caracter actual, se informa un error lexico con su ubicacion exacta.
    """
    tokens = []

    # PASO 1 - PREPARAR EL RECORRIDO Y LA UBICACION

    # Indice usado para recorrer cada caracter del texto desde cero.
    posicion = 0

    # Numero de linea actual. La primera linea es la 1.
    linea = 1

    # Columna del caracter actual. Tambien comienza en 1.
    columna = 1

    while posicion < len(texto):
        caracter = texto[posicion]

        # PASO 2 - CONSUMIR SEPARADORES Y TEXTO QUE NO GENERA TOKENS

        # Un salto avanza de linea y reinicia la columna.
        if caracter == "\n":
            posicion += 1
            linea += 1
            columna = 1
            continue

        # Los espacios separan tokens. Se consumen, pero no generan tokens.
        if caracter.isspace():
            posicion += 1
            columna += 1
            continue

        # Un comentario // se ignora hasta el final de la linea.
        if texto.startswith("//", posicion):
            while posicion < len(texto) and texto[posicion] != "\n":
                posicion += 1
                columna += 1
            # El salto queda pendiente para contabilizarlo en la siguiente vuelta.
            continue

        # PASO 3 - LEER LITERALES COMPLETOS

        # Literales numericos enteros y decimales.
        if caracter.isdigit():
            # Se guarda la columna antes de avanzar porque es la posicion
            # inicial que debe aparecer en el token.
            inicio = posicion
            columna_inicio = columna

            # Lee todos los digitos de la parte entera.
            while posicion < len(texto) and texto[posicion].isdigit():
                posicion += 1
                columna += 1

            # Un decimal admite un unico punto seguido de mas digitos.
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

                # Un segundo punto seguido de digitos forma un decimal invalido.
                if (
                    posicion + 1 < len(texto)
                    and texto[posicion] == "."
                    and texto[posicion + 1].isdigit()
                ):
                    raise ValueError(
                        f"Decimal mal formado en linea {linea}, "
                        f"columna {columna}"
                    )

            tokens.append(
                ("NUMERO", texto[inicio:posicion], linea, columna_inicio)
            )
            continue

        # Literales de texto entre comillas dobles.
        if caracter == '"':
            # La ubicacion del token y de un posible error es la comilla inicial.
            columna_inicio = columna
            posicion += 1
            columna += 1
            inicio = posicion

            # Las cadenas de este lexer no pueden continuar en otra linea.
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

        # PASO 4 - LEER Y CLASIFICAR PALABRAS COMPLETAS

        # Palabras usadas como nombres de variables.
        # Una palabra debe empezar con una letra.
        if caracter.isalpha():
            inicio = posicion
            columna_inicio = columna

            # Despues del primer caracter se aceptan letras, digitos y _.
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

            # La palabra completa se clasifica, nunca por prefijos.
            # Por eso "integer" es un IDENTIFICADOR y no "int" + "eger".
            if palabra in TIPOS:
                tipo = "TIPO"
            elif palabra in PALABRAS_RESERVADAS:
                tipo = "PALABRA_RESERVADA"
            else:
                tipo = "IDENTIFICADOR"

            tokens.append((tipo, palabra, linea, columna_inicio))
            continue

        # PASO 5 - RECONOCER OPERADORES Y SIMBOLOS

        # Se prueban primero los simbolos mas largos.
        posible_simbolo = texto[posicion:posicion + 2]

        if posible_simbolo in SIMBOLOS_DOBLES:
            tokens.append(("SIMBOLO", posible_simbolo, linea, columna))
            posicion += 2
            columna += 2
            continue

        # +, - y * generan tokens de tipo OPERADOR.
        if caracter in OPERADORES:
            tokens.append(("OPERADOR", caracter, linea, columna))
            posicion += 1
            columna += 1
            continue

        # = representa asignacion y ; finaliza la instruccion.
        # Los demas simbolos simples se procesan con la misma regla.
        if caracter in SIMBOLOS:
            tokens.append(("SIMBOLO", caracter, linea, columna))
            posicion += 1
            columna += 1
            continue

        # PASO 6 - INFORMAR EL ERROR SI NINGUNA REGLA COINCIDIO

        # Si ninguna regla reconoce el caracter, hay error lexico.
        raise ValueError(
            f"Caracter no reconocido {caracter!r} "
            f"en linea {linea}, columna {columna}"
        )

    return tokens
