# Lenguaje .nea

Proyecto del Grupo 11 para la materia Lenguajes Formales. `.nea` es un
lenguaje de programacion con palabras inspiradas en expresiones colombianas.

Integrantes:

- Esteban Pineda Ardila
- Cristian Felipe Lopez
- Steven Cardona

Las palabras reservadas y algunos ejemplos del lenguaje estan en
`lenguaje-colombiano.txt` y `palabras_reservadas.md`.

## Lexer

El lexer recibe codigo fuente y lo separa en tokens. Cada token guarda cuatro
datos:

```python
(tipo, texto, linea, columna)
```

Por ejemplo:

```python
from nea_lexer import tokenizar

print(tokenizar("numero edad = 20;"))
```

produce:

```python
[
    ("TIPO", "numero", 1, 1),
    ("IDENTIFICADOR", "edad", 1, 8),
    ("SIMBOLO", "=", 1, 13),
    ("NUMERO", "20", 1, 15),
    ("SIMBOLO", ";", 1, 17),
]
```

El segundo dato de cada tupla es el lexema: el texto exacto que se encontro en
el codigo. En el ejemplo anterior, `edad` y `20` son lexemas.

### Tipos de token

| Tipo | Ejemplos |
| --- | --- |
| `TIPO` | `numero`, `decimal`, `texto`, `booleano` |
| `IDENTIFICADOR` | `edad`, `total`, `nota_final2` |
| `PALABRA_RESERVADA` | `siPues`, `mientrasTinto`, `hablame` |
| `NUMERO` | `20`, `3.14` |
| `CADENA` | `"hola"` |
| `OPERADOR` | `+`, `-`, `*` |
| `SIMBOLO` | `=`, `;`, `>=`, `==` |

Los comentarios comienzan con `//` y se ignoran hasta el final de la linea.

## Estructura

```text
nea_lexer/
    __init__.py
    __main__.py
    lexer.py
tests/
    __init__.py
    test_lexer.py
lenguaje-colombiano.txt
palabras_reservadas.md
reglas.txt
README.md
```

La implementacion esta en `nea_lexer/lexer.py`. Todas las pruebas estan juntas
en `tests/test_lexer.py`.

## Preparar el entorno

Se necesita Python 3. Se puede comprobar la version instalada con:

```bash
python --version
```

Desde la carpeta del proyecto, crea el entorno virtual:

```bash
python -m venv .venv
```

Activalo con el comando correspondiente a tu terminal.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

Linux o macOS:

```bash
source .venv/bin/activate
```

Cuando este activo aparecera `(.venv)` al comienzo de la terminal.

Si PowerShell no permite ejecutar `Activate.ps1`, se puede habilitar solo para
la terminal actual:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

Tambien es posible usar el entorno sin activarlo:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

## Ejecutar el lexer

El paquete incluye unos ejemplos cortos:

```bash
python -m nea_lexer
```

Para probar otra entrada desde Python:

```python
from nea_lexer import tokenizar

codigo = 'texto nombre = "Ana";'
print(tokenizar(codigo))
```

## Ejecutar las pruebas

Para ejecutar todas las pruebas:

```bash
python -m unittest discover -v
```

Para ejecutar unicamente los seis casos de entrega:

```bash
python -m unittest tests.test_lexer.CasosEvaluacionLexer -v
```

Esos seis casos muestran en la terminal:

- la entrada;
- la salida calculada a mano;
- la salida real del lexer;
- una marca que indica si ambas coinciden.

Hay tres casos validos: una declaracion sencilla, una expresion sin espacios y
dos lineas con comentario. Los tres casos invalidos comprueban un caracter
desconocido, un decimal mal formado y una cadena sin cerrar en la segunda
linea.

Al final debe aparecer algo parecido a:

```text
Ran 25 tests

OK
```

## Como funciona

`tokenizar` recorre el texto de izquierda a derecha. `posicion` indica que
caracter se esta leyendo, mientras que `linea` y `columna` guardan su ubicacion.

El orden de las comprobaciones importa:

1. Los saltos de linea actualizan la linea y reinician la columna.
2. Los espacios y comentarios se consumen sin generar tokens.
3. Los numeros y las cadenas se leen completos.
4. Las palabras se leen completas antes de clasificarlas como tipo, reservada
   o identificador. Por eso `integer` no se divide en `int` y `eger`.
5. Los simbolos de dos caracteres se revisan antes que los de uno.
6. Si ninguna regla reconoce el caracter actual, se lanza un error con su linea
   y columna.

Una palabra debe comenzar con una letra. Despues puede contener letras,
digitos o `_`, como en `nota_final2`.

## Ejemplo para seguir a mano

Entrada:

```text
int total=a+5*2;
```

| Texto | Clasificacion | Linea | Columna |
| --- | --- | ---: | ---: |
| `int` | `TIPO` | 1 | 1 |
| `total` | `IDENTIFICADOR` | 1 | 5 |
| `=` | `SIMBOLO` | 1 | 10 |
| `a` | `IDENTIFICADOR` | 1 | 11 |
| `+` | `OPERADOR` | 1 | 12 |
| `5` | `NUMERO` | 1 | 13 |
| `*` | `OPERADOR` | 1 | 14 |
| `2` | `NUMERO` | 1 | 15 |
| `;` | `SIMBOLO` | 1 | 16 |

Este recorrido permite explicar de donde sale cada token y por que tiene esa
linea y columna.
