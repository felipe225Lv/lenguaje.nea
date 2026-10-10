# Lenguaje .nea

Proyecto del Grupo 11 para definir un lenguaje de programacion con sintaxis
inspirada en expresiones colombianas.

Integrantes:

- Esteban Pineda Ardila
- Cristian Felipe Lopez

## Reglas en lenguaje natural

1. Si la persona tiene 18 anos o mas, se considera mayor de edad.
2. Saber si un usuario esta activo.
3. Saber si hay dinero.
4. La persona debe ser mayor de edad y tener autorizacion.
5. Puede comprar si tiene suficiente dinero o tiene credito aprobado.
6. Debe ser mayor de edad y tener licencia.
7. Saber si alguien tiene el acceso permitido.
8. Es posible retirar dinero.
9. Si la compra es superior a cierto valor y el cliente es frecuente, recibe descuento.
10. Una persona puede ingresar si tiene invitacion o es empleado.
11. Si la gasolina es menor al minimo permitido, se muestra una advertencia.
12. Si el cliente tiene puntos suficientes y su cuenta esta activa, puede acceder a una promocion.
13. Si el vehiculo supera la velocidad maxima o el conductor no tiene autorizacion, se genera una advertencia.
14. Si la nota es igual o superior a 3.0, el estudiante aprueba.
15. Si el usuario tiene saldo suficiente y tiene un cupon, puede realizar la compra con beneficio.

## Variables del sistema

| Variable | Tipo en Java | Ejemplo de valor |
| --- | --- | --- |
| edad | int | 20 |
| activo | boolean | true |
| saldo | double | 150000.0 |
| autorizado | boolean | true |
| tieneLicencia | boolean | false |
| compra | double | 120000.0 |
| clienteFrecuente | boolean | true |
| tieneInvitacion | boolean | false |
| esEmpleado | boolean | true |
| gasolina | double | 8.5 |
| puntos | int | 650 |
| cuentaActiva | boolean | true |
| velocidad | double | 95.5 |
| velocidadMaxima | double | 80.0 |
| nota | double | 3.8 |
| tieneCupon | boolean | true |
| precio | double | 45000.0 |
| creditoAprobado | boolean | false |
| nombre | String | "Felipe" |
| usuario | String | null |

## Lexer

El proyecto incluye un lexer inicial para `.nea`. El lexer recibe texto fuente
y lo convierte en una lista de tokens con su tipo, contenido, linea y columna.

Cada token tiene la forma:

```python
(tipo, texto, linea, columna)
```

Ejemplo:

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

Tipos de token usados actualmente:

- `NUMERO`: numeros enteros o decimales, como `20` o `3.0`.
- `IDENTIFICADOR`: nombres de variables, como `edad`, `nota` o `nota_final2`.
- `PALABRA_RESERVADA`: palabras propias del lenguaje, como `siPues`.
- `SIMBOLO`: simbolos y operadores, como `;`, `(`, `)`, `>=` o `==`.

## Estructura del proyecto

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

Entra a la carpeta donde este este proyecto:

```bash
cd ruta/del/proyecto/lenguaje.nea
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

Cuando el entorno este activo, la terminal debe mostrar `(.venv)` al inicio.

## Ejecutar el lexer

Para ejecutar los ejemplos incluidos en el paquete:

```bash
python -m nea_lexer
```

## Ejecutar las pruebas

Con el entorno virtual activo, ejecuta:

```bash
python -m unittest discover -v
```

Este comando significa:

- `python -m unittest`: ejecuta el modulo de pruebas incluido en Python.
- `discover`: busca automaticamente archivos de prueba dentro del proyecto.
- `-v`: muestra informacion detallada de cada prueba.

Cada prueba imprime:

- `Entrada`: texto que se le pasa a `tokenizar`.
- `Esperado`: lista de tokens que deberia producir.
- `Obtenido`: lista de tokens producida realmente por el lexer.

Si todo esta bien, debe terminar con:

```text
OK
```

Tambien puedes ejecutar el archivo de pruebas directamente:

```bash
python -m unittest tests.test_lexer -v
```

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
creala otra vez.

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
