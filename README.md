# Orientación Proyecto AC

## Materiales

Para la realización del proyecto se entregan junto con este informe los siguientes materiales:

* Este documento (`README.md`)
* `smips.pdf`
* Scripts de Python para el testeo automático(`asambler.py`, `test.py` y `price.py`)
* Dos archivos punto circ `s-mips-template.circ` y `s-mips.circ`.
* Carpeta `tests` conteniendo diferentes archivos `.asm`

## Orientación

El objetivo de este proyecto es que puedan implementar usando `Logisim` una arquitectura para interpretar las instrucciones de S-MIPS. Los detalles relacionados a esta implementación estan descritos en el archivo [`s-mips.pdf`](./s-mips.pdf).

## Detalles de la evaluación

Se formarán equipos de hasta 2 integrantes para este proyecto. La entrega se realizará a través de GitHub. Un miembro de cada equipo deberá hacer un Fork [`Fork`](https://github.com/UH-Matcom-AC/Proyecto-SMIPS-2024-2025/fork) de este repositorio, donde desarrollarán su proyecto.

Posteriormente, deberán crear un nuevo `Issue` en la pestaña [Issues](https://github.com/UH-Matcom-AC/Proyecto-SMIPS-2024-2025/issues) de este repositorio. En el cuerpo del Issue, deben incluir los nombres completos de los integrantes, el grupo al que pertenece cada uno y la URL del proyecto generado a partir del `Fork`. Como referencia, pueden consultar el `Issue` de ejemplo: [`Equipo #0`](https://github.com/UH-Matcom-AC/Proyecto-SMIPS-2024-2025/issues/1). El título del `Issue` debe seguir el formato `Equipo #n`, donde `n` corresponde al número del equipo y debe respetar el orden de los `Issues` existentes.

La fecha límite para la entrega del proyecto es el 31 de enero de 2025 a las 11:59:59 PM. La entrega se considera automática, ya que no es necesario enviar archivos físicamente. Se tomarán en cuenta todos los commits realizados hasta la fecha límite como parte de la entrega del proyecto. Se recomienda que cada estudiante realice commits para documentar su trabajo individual, sugiriendo al menos un commit por cada componente implementado. Es fundamental evitar la creación de un único commit al final con todos los cambios del proyecto.

## Estructura de la plantilla

La plantilla consta de 3 componentes principales:

* CPU
* RAM
* RAM Dispatcher

La RAM es la componente que simulará la memoria RAM de una computadora. Esta no requiere de ningún cambio para que el microprocesador funcione. La interfaz a travéz de la cuál se utilizá estará descrita en el [`s-mips.pdf`](./s-mips.pdf). El RAM Dispatcher está estrechamente relacionado con la RAM y es necesario para la ejecución automática de los tests.

La CPU es la componente que usted deberá modificar para que interprete la instrucciones que cargue de la RAM y realice las operaciones correspondientes. Cualquier cambio fuera de esta componente será ignorado a la hora de hacer las revisiones por tanto limite cualquier cambio que considere importante a su interior.

## Tests Automáticos

El proyecto también incluye un conjunto de scripts en Python que permitirán realizar pruebas automáticas para conocer el estado actual del microprocesador y verificar que este funcione correctamente.

### Requisitos para utilizar los tests automáticos

Para poder ejecutar estos tests automáticos es necesario contar con los siguientes requisitos:

* Sistema Operativo Unix
* Python 3 instalado y accesible desde el comando `python3`
* Logisim instalado y accesible desde el comando `logisim`

### Pasos para ejecución

Una vez cumplidos los requisitos necesarios los tests pueden ser ejecutados mediante el siguiente comando:

```bash
./test.py tests s-mips.circ -o ./tests-out -t s-mips-template.circ
```

Este script dado un directorio escanea todos los ficheros `.asm` recursivamente dentro de dicho directorio y subdirectorios ensamblando el código de cada uno y generando los test correspondientes. Se espera encontrar dentro del fichero .asm una línea con un comentario de la siguiente forma:
**#prints** [:space:] *salida esperada*

Así cada test se ejecuta imprimiendo **OK** o **FAIL** en dependencia de si se obtuvo el resultado esperado o no. El script toma además varios niveles de verbosidad en el que brinda información más detallada de la ejecución.

### Agregar nuevos casos de prueba

Para crear nuevos casos de prueba se deberá crear un nuevo archivo `<test>.asm`. Es archivo contendrá el código que ejecutará el microprocesador. Estas instrucciones serán tomadas de las descritas en el [`s-mips.pdf`](./s-mips.pdf). Para definir cuál es el resultado correcto a mostrar por este código deberá estar definido una línea con el siguiente formato: `#prints <salida>`. Para mejor visualización de esto ver los casos de prueba existentes.

### Ejecución Manual

Para aquellos casos en los que se desee hacer un ejecución manual de uno de los casos de prueba se deben seguir los siguientes pasos:

1- Realizar el ensamblado de los casos de pruebas a utilizar. Para ello se debe usar el script `assembler.py`. Este recibe como parámetros el archivo con el código ensamblador y el directorio de salida. Ver la ayuda.

2- Una vez ejecutado el script buscar en la carpeta que existan 5 archivos llamados `Bank`, `Bank0`, `Bank1`, `Bank2` y `Bank3`.

3- Abrir en `logisim` el circuito `s-mips.circ`.

Opción 1 (Más sencilla):

4- Dejar desactivada la entrada nombrada `Deshabilitar Dispatcher`.

5- Luego se procede a cargar el archivos `Bank` dentro de la componente `RAM` del circuito `RAM Dispatcher`. Para ello debe entrar al circuito `RAM Dispatcher`, buscar en esta componente la componente `Bank` o también llamada `RAM`, y hacer click derecho sobre ella. Luego hacer click en cargar imagen. Finalmente seleccionar el archivo `Bank` correspondiente del caso de prueba a utilizar.

Opción 2 (Más compleja):

4- Activar la entrada nombrada `Deshabilitar Dispatcher`.

5- Luego se procede a cargar los archivos `Bank0`, `Bank1`, `Bank2` y `Bank3` dentro de la componente `RAM`. Para ello debe buscar en esta componente las etiquetas con nombres similares. Por cada componente `Bank`(llamada también `RAM` en logisim) hacer click derecho sobre ella, hacer click en cargar imagen, y finalmente seleccionar el archivo `Bank#` correspondiente con el número del `Bank` y según el caso de prueba a utilizar. Importante asegurarse de haber utilizado los bancos correctos. La búsqueda al cargar imagen recuerda direcciones separadas del resto.

Por último y común para cualquier opción:

6- Conmutar el reloj. Si todos los pasos fueron seguidos de forma correcta el microprocesador deberá empezar a ejecutar las instrucciones almacenadas ahora en la RAM.

### Requisitos

Para considerar un microprocesador como válido se deberán cumplir dos requisitos de precio, eficiencia y correctitud.

La correctitud se tomará en base a un conjunto de casos de pruebas que incluye los entregados con esta plantilla. En cada caso de prueba la salida de su microproseador por pantalla deberá coincidir con la salida establecida por la línea `#prints <salida>` en el caso de prueba. La salida de su microprocesador es aquella resultante de la ejecución de la instrucción `tty` en el código.

Junto al proyecto se entrega otro script de python `price.py` que permite dado un archivo `circ` calcular un precio del microprocesador. Dicho precio se calcula en base a las componentes utilizadas para la creación del mismo. El precio de un microprocesador para ser aceptado tendrá que tener un precio menor o igual a las `100` unidades.

La eficiencia será medida en base a la cantidad de ciclos del reloj que toma completar un caso de prueba determinado. Este límite estará dado por `x` ciclos del reloj. Esto será establecido para cada caso de prueba. El número exacto para un caso de prueba estará dado por la línea `#limit <cant-iterciones>`. El número exacto no está definido aún para todos los tests pero si será tomado en cuenta a la hora de la evaluación.

### Precisiones Adicionales

Para el correcto funcionamiento de los tests automáticos las componentes `RAM` de `logisim` (no la `RAM` implementada en la plantilla) utilizadas en el `s-mips.circ` deben cumplir ciertas condiciones. Para evitar conflictos, y puesto que tampoco es necesario, queda prohibido utilizar dichas componentes como partes de alguna de las componentes a implementar.
