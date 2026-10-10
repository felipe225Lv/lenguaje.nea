import unittest

from nea_lexer import tokenizar


class LexerTest(unittest.TestCase):
    def comparar_tokens(self, texto, esperado):
        obtenido = tokenizar(texto)

        print()
        print(f"Entrada: {texto!r}")
        print(f"Esperado: {esperado}")
        print(f"Obtenido: {obtenido}")

        self.assertEqual(obtenido, esperado)

    def test_numero_y_simbolo_tienen_columna(self):
        """Reconoce un numero y un simbolo con sus columnas iniciales."""
        self.comparar_tokens("20;", [("NUMERO", "20", 1, 1), ("SIMBOLO", ";", 1, 3)])

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

    def test_palabra_reservada_del_lenguaje(self):
        """Distingue una palabra reservada del lenguaje de un identificador."""
        self.comparar_tokens("siPues", [("PALABRA_RESERVADA", "siPues", 1, 1)])

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
