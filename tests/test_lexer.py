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


if __name__ == "__main__":
    unittest.main(verbosity=2)
