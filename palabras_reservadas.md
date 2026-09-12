
=====================================
Sintaxis general de las reglas
=====================================

<programa> ::= { <sentencia> }

<sentencia> ::= <estructura_condicional>
              | <llamada_funcion>


<estructura_condicional> ::= 
    "siPues" "(" <expresion_logica> ")" 
    "{" <bloque> "}" 
    [ <bloque_sino> ]


<bloque_sino> ::= 
    "siNoSiPues" "(" <expresion_logica> ")" 
    "{" <bloque> "}" 
    [ <bloque_sino> ]
    |
    "siNoPues" "{" <bloque> "}"


<bloque> ::= { <sentencia> }


<llamada_funcion> ::= 
    "hablame" "(" <expresion> ")"


<expresion> ::= <expresion_logica>
              | <valor_numerico>
              | <valor_booleano>
              | <cadena>


<expresion_logica> ::= 
    <termino_logico> 
    { <operador_logico> <termino_logico> }


<termino_logico> ::= 
    <comparacion>
    | <valor_booleano>
    | "(" <expresion_logica> ")"


<comparacion> ::= 
    <valor> <operador_relacional> <valor>


<valor> ::= 
    <valor_numerico>
    | <valor_booleano>


<operador_logico> ::= 
    "yTambien"
    | "oQue"


<operador_relacional> ::= 
    "==" 
    | "!=" 
    | ">"
    | "<"
    | ">="
    | "<="


<valor_booleano> ::= 
    "deUna"
    | "niRiesgo"


<valor_numerico> ::= 
    <digito> { <digito> } 
    [ "." <digito> { <digito> } ]


<cadena> ::= 
    '"' { <caracter> } '"'


<digito> ::= 
    "0" | "1" | "2" | "3" | "4" 
    | "5" | "6" | "7" | "8" | "9"


<letra> ::= 
    "a" | ... | "z"
    | "A" | ... | "Z"
=====================================
Tablas de palabras reservadas
=====================================
Concepto        | Palabra reservada     | Ejemplo
----------------|------------------------|----------------------------------------
print           | hablame                | hablame("Quiubo pues")
null            | sinPalabras            | usuario = sinPalabras
break           | yaEsta                 | yaEsta
continue        | sigaPues               | sigaPues
while           | mientrasTinto          | mientrasTinto (condicion)
if              | siPues                 | siPues (edad >= 18)
else            | siNoPues               | siNoPues
else if         | siNoSiPues             | siNoSiPues (...)
for             | paraPues               | paraPues (i = 0; i < 10; i++)
return          | devuelvame             | devuelvame resultado
function        | hagaUnaVuelta          | hagaUnaVuelta calcular()
class           | parche                 | parche Persona
new             | armeUno                | armeUno Persona()
this            | esteMan                | esteMan.nombre
super           | elPatron               | elPatron()
extends         | heredaDe               | parche Perro heredaDe Animal
import          | traigame               | traigame matematicas
export          | mandePues              | mandePues calcular
try             | aVerQuePasa            | aVerQuePasa { ... }
catch           | siSeEmputa             | siSeEmputa { ... }
finally         | paseLoQuePase          | paseLoQuePase { ... }
throw           | tireLaBomba            | tireLaBomba error
true            | deUna                  | activo = deUna
false           | niRiesgo               | activo = niRiesgo
and             | yTambien               | edad > 18 yTambien activo
or              | oQue                   | rojo oQue azul
not             | niDeRiesgo             | niDeRiesgo activo
const           | esoQuedaAsi            | esoQuedaAsi PI = 3.14
let             | dejeEso                | dejeEso nombre = "Felipe"
var             | unaVariable            | unaVariable edad = 20
switch          | segunElCaso            | segunElCaso opcion
case            | enEsteCaso             | enEsteCaso 1:
default         | siNadaDeEso            | siNadaDeEso:
async           | conCalma               | conCalma hagaAlgo()
await           | espereUnMomentico      | espereUnMomentico respuesta

=====================================
Convención de escritura del proyecto
=====================================

1. Palabras reservadas → siempre en camelCase, empezando con minúscula.
Ejemplos: siPues, siNoPues, mientrasTinto, hagaUnaVuelta, tireLaBomba.

2. Nombres de variables → camelCase, sustantivo o adjetivo descriptivo, sin abreviar salvo que sea obvio (edad, no ed).
Ejemplos: saldo, activo, tieneLicencia, clienteFrecuente, velocidadMaxima.

Las variables booleanas empiezan con un prefijo que deje claro que es sí/no: tiene..., es..., esta... (tieneCupon, esEmpleado, cuentaActiva).
Las variables numéricas usan el nombre del concepto sin prefijo (edad, saldo, puntos, nota).

3. Nombres de "parches" (clases) → PascalCase (primera letra mayúscula), ya que en tu tabla parche Persona, parche Perro siguen ese patrón.

4. Constantes (esoQuedaAsi) → MAYÚSCULAS_CON_GUION_BAJO, como en tu ejemplo esoQuedaAsi PI = 3.14 → sería PI. Si el nombre tiene varias palabras: TASA_INTERES.

5. Cadenas de texto (strings) → siempre entre comillas dobles "...", con mensajes en tono coloquial colombiano coherente con el resto del lenguaje (como ya haces: "Hagale pues, puede comprar").

6. Indentación y llaves → 4 espacios por nivel, llave de apertura { en la misma línea que la condición, llave de cierre } alineada con el siPues/mientrasTinto que la abre. Así:

siPues (edad >= 18) {
    hablame("Ya es mayor de edad, parce")
}

7. Operadores relacionales y lógicos → siempre con un espacio antes y después (edad >= 18, no edad>=18), y las palabras reservadas lógicas (yTambien, oQue) también rodeadas de espacio.

8. Comentarios (si el lenguaje los llega a soportar) → se recomienda un estilo coherente con el tema, por ejemplo // nota: o similar, aunque esto lo puedes dejar como trabajo futuro si no lo tienes definido aún.