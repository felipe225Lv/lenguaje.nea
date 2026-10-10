# Lexer para lenguaje .nea

Este proyecto contiene un lexer inicial para el lenguaje colombiano `.nea`.
El lexer recibe texto fuente y lo convierte en una lista de tokens con su
tipo, contenido, linea y columna.

## Estructura

```text
nea_lexer/
    __init__.py
    __main__.py
    lexer.py
tests/
    __init__.py
    test_lexer.py
README.md
```

## Requisitos

- Python 3.12 o superior.
- Una terminal: PowerShell, CMD, Terminal de macOS o una terminal de Linux.

Para verificar que Python esta instalado:

```bash
python --version
```

Ejemplo de salida:

```text
Python 3.12.10
```

## Preparar el proyecto

Entra a la carpeta donde este este proyecto. Por ejemplo:

```bash
cd ruta/del/proyecto/lexer
```

Crea el entorno virtual:

```bash
python -m venv .venv
```

Activa el entorno virtual segun tu sistema operativo.

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

Cuando el entorno este activo, la terminal debe mostrar `(.venv)` al inicio:

```text
(.venv) ...
```

## Uso

Para ejecutar los ejemplos incluidos en el paquete:

```bash
python -m nea_lexer
```

Para usar el lexer desde otro archivo Python:

```python
from nea_lexer import tokenizar

print(tokenizar("5;\n12;"))
```

Salida esperada:

```python
[
    ("NUMERO", "5", 1, 1),
    ("SIMBOLO", ";", 1, 2),
    ("NUMERO", "12", 2, 1),
    ("SIMBOLO", ";", 2, 3),
]
```

Cada token tiene la forma:

```python
(tipo, texto, linea, columna)
```

Tipos de token usados actualmente:

- `NUMERO`: numeros enteros o decimales, como `20` o `3.0`.
- `IDENTIFICADOR`: nombres de variables, como `edad`, `nota` o `nota_final2`.
- `PALABRA_RESERVADA`: palabras propias del lenguaje, como `siPues`.
- `SIMBOLO`: simbolos y operadores, como `;`, `(`, `)`, `>=` o `==`.

## Como funciona el algoritmo

El lexer lee el texto caracter por caracter, de izquierda a derecha.
Mientras avanza guarda tres datos importantes:

- `posicion`: indice actual dentro del texto.
- `linea`: numero de linea actual, empezando en 1.
- `columna`: columna actual, empezando en 1.

Cuando encuentra un salto de linea (`\n`), aumenta `linea` y reinicia
`columna` a 1.

Cuando encuentra un numero, sigue leyendo mientras aparezcan mas digitos.
Tambien acepta decimales como `3.0`.

Cuando encuentra una letra, sigue leyendo mientras aparezcan letras, digitos
o `_`. Luego revisa si esa palabra esta en la tabla de palabras reservadas.
Si esta, genera `PALABRA_RESERVADA`; si no, genera `IDENTIFICADOR`.

Los operadores de dos caracteres, como `>=`, `<=`, `==` y `!=`, se revisan
antes que los simbolos de un solo caracter para no separarlos por error.

## Pruebas

Con el entorno virtual activo, ejecuta:

```bash
python -m unittest discover -v
```

Este comando significa:

- `python -m unittest`: ejecuta el modulo de pruebas incluido en Python.
- `discover`: busca automaticamente archivos de prueba dentro del proyecto.
- `-v`: muestra informacion detallada de cada prueba.

Si todo esta bien, debe terminar con:

```text
OK
```

Cada prueba imprime:

- `Entrada`: texto que se le pasa a `tokenizar`.
- `Esperado`: lista de tokens que deberia producir.
- `Obtenido`: lista de tokens producida realmente por el lexer.

Tambien puedes ejecutar el archivo de pruebas directamente:

```bash
python -m unittest tests.test_lexer -v
```

## Errores comunes

### PowerShell no deja activar el entorno

Si aparece un error como:

```text
la ejecucion de scripts esta deshabilitada en este sistema
```

Ejecuta una sola vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Luego intenta activar de nuevo:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Python no aparece

Si `python --version` dice que Python no existe, instala Python y vuelve a
abrir la terminal.

### El entorno virtual quedo mal creado

Si `.venv` apunta a una ruta vieja de Python, borra la carpeta `.venv` y
creala otra vez:

En Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
```
