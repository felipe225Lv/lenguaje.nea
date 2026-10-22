"""Pruebas automatizadas del lexer del lenguaje .nea.

Organizacion del archivo:
- PruebasUnitariasLexer: verifica cada funcionalidad de forma aislada.
- CasosEvaluacionLexer: ejecuta los seis casos finales con reporte detallado.

Las pruebas unitarias no imprimen datos cuando pasan. Los casos finales si
muestran entrada, calculo manual, salida real y una conclusion explicita.
"""

import sys
import unittest

from nea_lexer import tokenizar


class PruebasUnitariasLexer(unittest.TestCase):
    """Verifica de manera aislada cada capacidad del analizador lexico."""

    def comparar_tokens(self, texto, esperado):
        """Compara tokens sin imprimir ruido cuando la prueba es correcta."""
        obtenido = tokenizar(texto)
        self.assertEqual(obtenido, esperado)

    # Tarea 1: columna inicial de cada token.

    def test_numero_y_simbolo_tienen_columna(self):
        """Reconoce un numero y un simbolo con sus columnas iniciales."""
        self.comparar_tokens("20;", [("NUMERO", "20", 1, 1), ("SIMBOLO", ";", 1, 3)])

    # Tarea 2: saltos de linea y reinicio de columna.

    def test_salto_de_linea_reinicia_columna(self):
        """Reconoce saltos de linea y reinicia la columna en la nueva linea."""
        self.comparar_tokens(
            "5;\n12;",
            [
                ("NUMERO", "5", 1, 1),
                ("SIMBOLO", ";", 1, 2),
                ("NUMERO", "12", 2, 1),
                ("SIMBOLO", ";", 2, 3),
            ],
        )

    # Tarea 3: identificadores completos.

    def test_palabras_son_identificadores(self):
        """Reconoce nombres de variables como identificadores completos."""
        self.comparar_tokens(
            "edad nota",
            [
                ("IDENTIFICADOR", "edad", 1, 1),
                ("IDENTIFICADOR", "nota", 1, 6),
            ],
        )

    def test_identificador_puede_continuar_con_digitos_y_guion_bajo(self):
        """Permite letras, digitos y guion bajo despues de la primera letra."""
        self.comparar_tokens("nota_final2", [("IDENTIFICADOR", "nota_final2", 1, 1)])

    def test_identificador_debe_empezar_con_letra(self):
        """Rechaza un guion bajo como primer caracter de un identificador."""
        with self.assertRaisesRegex(
            ValueError, r"linea 1, columna 1"
        ):
            tokenizar("_nota")

    # Tarea 4: tipos, palabras reservadas e identificadores.

    def test_tipos_de_datos(self):
        """Distingue tipos de datos de identificadores completos."""
        self.comparar_tokens(
            "numero edad integer",
            [
                ("TIPO", "numero", 1, 1),
                ("IDENTIFICADOR", "edad", 1, 8),
                ("IDENTIFICADOR", "integer", 1, 13),
            ],
        )

    def test_palabra_reservada_del_lenguaje(self):
        """Distingue una palabra reservada del lenguaje de un identificador."""
        self.comparar_tokens("siPues", [("PALABRA_RESERVADA", "siPues", 1, 1)])

    # Tarea 5: asignacion, fin de instruccion y simbolos largos primero.

    def test_declaracion_completa(self):
        """Reconoce tipo, variable, asignacion, valor y fin de instruccion."""
        self.comparar_tokens(
            "numero edad = 20;",
            [
                ("TIPO", "numero", 1, 1),
                ("IDENTIFICADOR", "edad", 1, 8),
                ("SIMBOLO", "=", 1, 13),
                ("NUMERO", "20", 1, 15),
                ("SIMBOLO", ";", 1, 17),
            ],
        )

    def test_decimal_y_operador_doble(self):
        """Reconoce numeros decimales y operadores de dos caracteres."""
        self.comparar_tokens(
            "nota >= 3.0",
            [
                ("IDENTIFICADOR", "nota", 1, 1),
                ("SIMBOLO", ">=", 1, 6),
                ("NUMERO", "3.0", 1, 9),
            ],
        )

    # Tarea 6: comentarios ignorados sin alterar las posiciones.

    def test_comentario_al_final_de_declaracion(self):
        """Ignora el comentario y conserva los tokens de la declaracion."""
        self.comparar_tokens(
            "numero edad = 20; // esto se ignora",
            [
                ("TIPO", "numero", 1, 1),
                ("IDENTIFICADOR", "edad", 1, 8),
                ("SIMBOLO", "=", 1, 13),
                ("NUMERO", "20", 1, 15),
                ("SIMBOLO", ";", 1, 17),
            ],
        )

    def test_comentario_no_altera_la_siguiente_linea(self):
        """Ignora el comentario y conserva el numero de linea siguiente."""
        self.comparar_tokens(
            "numero edad = 20; // comentario\nnumero saldo = 50;",
            [
                ("TIPO", "numero", 1, 1),
                ("IDENTIFICADOR", "edad", 1, 8),
                ("SIMBOLO", "=", 1, 13),
                ("NUMERO", "20", 1, 15),
                ("SIMBOLO", ";", 1, 17),
                ("TIPO", "numero", 2, 1),
                ("IDENTIFICADOR", "saldo", 2, 8),
                ("SIMBOLO", "=", 2, 14),
                ("NUMERO", "50", 2, 16),
                ("SIMBOLO", ";", 2, 18),
            ],
        )

    # Tarea 6.1: errores lexicos con linea y columna.

    def test_error_lexico_indica_linea_y_columna(self):
        """Informa la ubicacion exacta de un caracter desconocido."""
        with self.assertRaisesRegex(
            ValueError, r"linea 1, columna 18"
        ):
            tokenizar("numero edad = 20 @")

    def test_error_lexico_en_segunda_linea(self):
        """Informa correctamente la ubicacion del error en otra linea."""
        with self.assertRaisesRegex(
            ValueError, r"linea 2, columna 1"
        ):
            tokenizar("numero edad = 20;\n@")

    # Tarea 6.2: decimales y cadenas de texto.

    def test_declaracion_con_decimal(self):
        """Reconoce un literal decimal completo en una declaracion."""
        self.comparar_tokens(
            "double precio = 3.14;",
            [
                ("TIPO", "double", 1, 1),
                ("IDENTIFICADOR", "precio", 1, 8),
                ("SIMBOLO", "=", 1, 15),
                ("NUMERO", "3.14", 1, 17),
                ("SIMBOLO", ";", 1, 21),
            ],
        )

    def test_literal_de_texto(self):
        """Reconoce una cadena completa entre comillas dobles."""
        self.comparar_tokens(
            'texto saludo = "hola";',
            [
                ("TIPO", "texto", 1, 1),
                ("IDENTIFICADOR", "saludo", 1, 7),
                ("SIMBOLO", "=", 1, 14),
                ("CADENA", "hola", 1, 16),
                ("SIMBOLO", ";", 1, 22),
            ],
        )

    def test_cadena_sin_cerrar_indica_linea_de_inicio(self):
        """Informa la linea donde comenzo una cadena sin comilla de cierre."""
        with self.assertRaisesRegex(
            ValueError, r"Cadena sin cerrar en linea 2, columna 16"
        ):
            tokenizar('numero edad = 20;\ntexto saludo = "hola')

    # Tarea 6.3: operadores aritmeticos de un caracter.

    def test_operadores_aritmeticos_con_espacios(self):
        """Clasifica + y * como operadores y conserva sus columnas."""
        self.comparar_tokens(
            "int total = a + 5 * 2;",
            [
                ("TIPO", "int", 1, 1),
                ("IDENTIFICADOR", "total", 1, 5),
                ("SIMBOLO", "=", 1, 11),
                ("IDENTIFICADOR", "a", 1, 13),
                ("OPERADOR", "+", 1, 15),
                ("NUMERO", "5", 1, 17),
                ("OPERADOR", "*", 1, 19),
                ("NUMERO", "2", 1, 21),
                ("SIMBOLO", ";", 1, 22),
            ],
        )

    def test_operadores_aritmeticos_sin_espacios(self):
        """Reconoce operadores aunque no tengan espacios alrededor."""
        self.comparar_tokens(
            "a+5*2",
            [
                ("IDENTIFICADOR", "a", 1, 1),
                ("OPERADOR", "+", 1, 2),
                ("NUMERO", "5", 1, 3),
                ("OPERADOR", "*", 1, 4),
                ("NUMERO", "2", 1, 5),
            ],
        )

    def test_operador_resta(self):
        """Clasifica el signo menos como operador aritmetico."""
        self.comparar_tokens(
            "total-1",
            [
                ("IDENTIFICADOR", "total", 1, 1),
                ("OPERADOR", "-", 1, 6),
                ("NUMERO", "1", 1, 7),
            ],
        )

# Tarea 7: seis casos finales solicitados para la entrega del parcial.
class CasosEvaluacionLexer(unittest.TestCase):
    """Seis casos calculados a mano para la entrega del parcial."""

    SEPARADOR = "=" * 78

    def imprimir_encabezado(self, numero, titulo, entrada):
        """Muestra el caso y numera las lineas de la entrada."""
        print(file=sys.stderr)
        print(self.SEPARADOR, file=sys.stderr)
        print(f"CASO {numero}: {titulo}", file=sys.stderr)
        print(self.SEPARADOR, file=sys.stderr)
        print("ENTRADA:", file=sys.stderr)

        for numero_linea, contenido in enumerate(entrada.splitlines(), start=1):
            print(f"  {numero_linea:>2} | {contenido}", file=sys.stderr)

    def imprimir_tokens(self, etiqueta, tokens):
        """Imprime los tokens como una tabla para comparar sus cuatro datos."""
        ancho_tipo = max([len("TIPO"), *(len(tipo) for tipo, _, _, _ in tokens)])
        ancho_texto = max(
            [len("TEXTO"), *(len(repr(texto)) for _, texto, _, _ in tokens)]
        )

        print(f"\n{etiqueta}:", file=sys.stderr)
        print(
            f"  {'#':>2} | {'TIPO':<{ancho_tipo}} | "
            f"{'TEXTO':<{ancho_texto}} | {'LINEA':>5} | {'COLUMNA':>7}",
            file=sys.stderr,
        )
        print(
            f"  {'-' * 2}-+-{'-' * ancho_tipo}-+-"
            f"{'-' * ancho_texto}-+-{'-' * 5}-+-{'-' * 7}",
            file=sys.stderr,
        )

        for numero, (tipo, texto, linea, columna) in enumerate(tokens, start=1):
            print(
                f"  {numero:>2} | {tipo:<{ancho_tipo}} | "
                f"{texto!r:<{ancho_texto}} | {linea:>5} | {columna:>7}",
                file=sys.stderr,
            )

    def imprimir_resultado(self, coinciden):
        """Cierra el bloque con una marca facil de identificar."""
        estado = "SI, COINCIDEN" if coinciden else "NO, HAY DIFERENCIAS"
        print(f"\nRESULTADO: {estado}", file=sys.stderr)
        print(self.SEPARADOR, file=sys.stderr, flush=True)

    def comparar_caso_valido(self, numero, titulo, entrada, esperado):
        """Ejecuta un caso valido y presenta ambas listas de tokens."""
        self.imprimir_encabezado(numero, titulo, entrada)
        self.imprimir_tokens("SALIDA ESPERADA (calculada a mano)", esperado)

        obtenido = tokenizar(entrada)
        coinciden = obtenido == esperado

        self.imprimir_tokens("SALIDA REAL DEL LEXER", obtenido)
        self.imprimir_resultado(coinciden)

        self.assertTrue(
            coinciden,
            "La salida calculada a mano no coincide con la salida del lexer",
        )

    def comparar_caso_invalido(self, numero, titulo, entrada, error_esperado):
        """Ejecuta un caso invalido y compara los mensajes de error."""
        self.imprimir_encabezado(numero, titulo, entrada)
        print(f"\nERROR ESPERADO:\n  {error_esperado}", file=sys.stderr)

        try:
            tokenizar(entrada)
        except ValueError as error:
            error_obtenido = str(error)
        else:
            error_obtenido = "NO SE PRODUJO NINGUN ERROR"

        coinciden = error_obtenido == error_esperado

        print(f"\nERROR REAL DEL LEXER:\n  {error_obtenido}", file=sys.stderr)
        self.imprimir_resultado(coinciden)

        self.assertTrue(
            coinciden,
            "El error calculado a mano no coincide con el error del lexer",
        )

    def test_01_declaracion_valida_con_espacios(self):
        """Caso valido simple: declaracion de una variable numerica."""
        esperado = [
            ("TIPO", "numero", 1, 1),
            ("IDENTIFICADOR", "edad", 1, 8),
            ("SIMBOLO", "=", 1, 13),
            ("NUMERO", "20", 1, 15),
            ("SIMBOLO", ";", 1, 17),
        ]

        self.comparar_caso_valido(
            1,
            "VALIDO SIMPLE CON ESPACIOS",
            "numero edad = 20;",
            esperado,
        )

    def test_02_declaracion_valida_sin_espacios(self):
        """Caso valido sin espacios entre identificadores y operadores."""
        esperado = [
            ("TIPO", "int", 1, 1),
            ("IDENTIFICADOR", "total", 1, 5),
            ("SIMBOLO", "=", 1, 10),
            ("IDENTIFICADOR", "a", 1, 11),
            ("OPERADOR", "+", 1, 12),
            ("NUMERO", "5", 1, 13),
            ("OPERADOR", "*", 1, 14),
            ("NUMERO", "2", 1, 15),
            ("SIMBOLO", ";", 1, 16),
        ]

        self.comparar_caso_valido(
            2,
            "VALIDO SIN ESPACIOS Y CON OPERADORES",
            "int total=a+5*2;",
            esperado,
        )

    def test_03_dos_lineas_con_comentario(self):
        """Caso valido con comentario y tokens en una segunda linea."""
        entrada = 'numero edad = 20; // comentario\ntexto nombre = "Ana";'
        esperado = [
            ("TIPO", "numero", 1, 1),
            ("IDENTIFICADOR", "edad", 1, 8),
            ("SIMBOLO", "=", 1, 13),
            ("NUMERO", "20", 1, 15),
            ("SIMBOLO", ";", 1, 17),
            ("TIPO", "texto", 2, 1),
            ("IDENTIFICADOR", "nombre", 2, 7),
            ("SIMBOLO", "=", 2, 14),
            ("CADENA", "Ana", 2, 16),
            ("SIMBOLO", ";", 2, 21),
        ]

        self.comparar_caso_valido(
            3,
            "VALIDO CON DOS LINEAS, COMENTARIO Y CADENA",
            entrada,
            esperado,
        )

    def test_04_caracter_desconocido(self):
        """Caso invalido: @ no pertenece al lenguaje."""
        self.comparar_caso_invalido(
            4,
            "INVALIDO POR CARACTER DESCONOCIDO",
            "numero edad = 20 @",
            "Caracter no reconocido '@' en linea 1, columna 18",
        )

    def test_05_decimal_mal_formado(self):
        """Caso invalido: un decimal no puede contener dos puntos."""
        self.comparar_caso_invalido(
            5,
            "INVALIDO POR DECIMAL MAL FORMADO",
            "decimal precio = 3.4.5;",
            "Decimal mal formado en linea 1, columna 21",
        )

    def test_06_error_en_segunda_linea(self):
        """Caso invalido: una cadena queda sin cerrar en la segunda linea."""
        self.comparar_caso_invalido(
            6,
            "INVALIDO EN LA SEGUNDA LINEA",
            'numero edad = 20;\ntexto nombre = "Ana',
            "Cadena sin cerrar en linea 2, columna 16",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
