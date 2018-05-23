# Inteligencia Artificial

Instituto Tecnológico de Costa Rica  
Ingeniería en Computación  
IC6200 - Inteligencia Artificial  
I Semestre, 2018

# Grupo #8

Fabio Mora Cubillo - 2013012801  
Sergio Moya Valerín - 2013015682  
Gabriel Venegas Castro - 2013115967

# Contenidos

Proyecto Corto 2 y 3 - Conejo y Zanahorias
 > + Algoritmo A*  
 > +---- Descripción  
 > +---- Cálculo de heuristico  
 > +---- Ejemplo  
 > +---- Análisis  
 > + Algoritmo Genético 
 > +---- Descripción
 > +---- Problemas potenciales detectados
 > +---- Ejemplo  
 > +---- Análisis  
 > + Apéndice  
 > +---- Instalación  
 > +---- Uso  
 > +---- Archivos de entrada  

# Algoritmo A*

## Calculo de heurístico

La pregunta que uno se debe hacer es cómo calcular **h**. Tenemos que el conejo tiene visión limitada, por lo que sabemos que tenemos que utilizar un heurístico por aproximación. Esto nos limita a tres opciones: "Euclidean Distance", "Manhattan Distance", "Diagonal Distance".
Como sabemos que en el algoritmo solo se puede mover el conejo en cuatro direcciones (arriba, abajo, izquierda y derecha) entonces se sabe que para el heurístico se debe utilizar la distancia Manhattan, que consiste en obtener el valor absoluto de las diferencias de las posiciones (x, y) del nodo actual con el nodo destino.

```python
def heuristic(node_1, node_2):
    """ Heuristic when only 4 directions are possible (Manhattan) """
    (x_node_1, y_node_1) = node_1
    (x_node_2, y_node_2) = node_2
    return abs(x_node_1 - x_node_2) + abs(y_node_1 - y_node_2)
```

## Ejemplo

Vision del conejo: 10  
Zanahorias a comer: 2  
Tablero inicial: 4x4 (con total de 2 zanahorias)

### Paso 00001
```
 CZ 
    
   Z
    
```
Podemos notar que en la posición derecha al conejo hay una zanahoria, esto implica que el conejo va a querer ir ahí, por lo que ese sería su nodo destino.

| Nodo | Posicion |f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(0, 2)` | `0` |
| Izquierda | `(0, 0)` | `3` |
| Derecha | `(0, 2)` | `1` |
| Abajo | `(1, 1)` | `3` |
| Arriba | `N/A` | `N/A` |

**Decisión**: Moverse hacia la derecha  
**Cálculos realizados**(directamente impresos por el algoritmo):  
```bash
(0, 1) -> (0, 0)  >>>  3  =  1  +  2
(0, 1) -> (1, 1)  >>>  3  =  1  +  2
(0, 1) -> (0, 2)  >>>  1  =  1  +  0
```
**Se imprime en consola**:  
```bash
PASO: 00001 IZQUIERDA: 3 DERECHA: 1 ARRIBA: N/A ABAJO: 3 MOVIMIENTO: DERECHA
```

### Paso 00002
```
  C 
    
   Z
    
```
En el paso anterior el conejo devoró una zanahoria, por lo que debe buscar otra. Podemos notar que el conejo puede ver una zanahoria a lo lejos, esto implica que el conejo va a querer ir ahí, por lo que ese sería su nodo destino.

| Nodo | Posicion | f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(0, 2)` | `0` |
| Izquierda | `(0, 1)` | `5` |
| Derecha | `(0, 3)` | `3` |
| Abajo | `(1, 2)` | `5` |
| Arriba | `N/A` | `N/A` |

**Decisión**: Moverse hacia la derecha  
**Cálculos realizados**(directamente impresos por el algoritmo):  
```bash
(0, 2) -> (0, 1)  >>>  5  =  1  +  4
(0, 2) -> (1, 2)  >>>  3  =  1  +  2
(0, 2) -> (0, 3)  >>>  3  =  1  +  2
(0, 3) -> (1, 3)  >>>  3  =  2  +  1
(1, 2) -> (1, 1)  >>>  5  =  2  +  3
(1, 2) -> (2, 2)  >>>  3  =  2  +  1
(1, 3) -> (2, 3)  >>>  3  =  3  +  0
(2, 2) -> (2, 1)  >>>  5  =  3  +  2
(2, 2) -> (3, 2)  >>>  5  =  3  +  2
```
**Se imprime en consola**:  
```bash
PASO: 00002 IZQUIERDA: 5 DERECHA: 3 ARRIBA: N/A ABAJO: 5 MOVIMIENTO: DERECHA 
```

### Paso 00003
```
   C
    
   Z
    
```
Como el conejo no ha comido ninguna zanahoria, se continúa con la búsqueda.

| Nodo | Posición |f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(0, 3)` | `0` |
| Izquierda |`(0, 2)` | `4` |
| Derecha | `N/A` | `N/A` |
| Abajo | `(1, 3)` | `2` |
| Arriba | `N/A` | `N/A` |

**Decisión**: Moverse hacia la derecha  
**Cálculos realizados**(directamente impresos por el algoritmo):  
```bash
(0, 3) -> (0, 2)  >>>  4  =  1  +  3
(0, 3) -> (1, 3)  >>>  2  =  1  +  1
(1, 3) -> (1, 2)  >>>  4  =  2  +  2
(1, 3) -> (2, 3)  >>>  2  =  2  +  0
```
**Se imprime en consola**:  
```bash
PASO: 00003 IZQUIERDA: 4 DERECHA: N/A ARRIBA: N/A ABAJO: 2 MOVIMIENTO: ABAJO 
```

### Paso 00004
```
    
   C
   Z
    
```
Como el conejo no ha comido ninguna zanahoria, se continúa con la búsqueda. Al estar la zanahoria en un nodo adyacente, la siguiente acción será devorarla. 

| Nodo | Posicion |f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(1, 3)` | `0` |
| Izquierda | `(1, 2)` | `3` |
| Derecha | `N/A` | `N/A` |
| Abajo | `(2, 3)` | `1` |
| Arriba | `(0, 3)` | `3` |

**Decisión**: Moverse hacia la derecha  
**Cálculos realizados**(directamente impresos por el algoritmo):  
```bash
(1, 3) -> (0, 3)  >>>  3  =  1  +  2
(1, 3) -> (1, 2)  >>>  3  =  1  +  2
(1, 3) -> (2, 3)  >>>  1  =  1  +  0
```
**Se imprime en consola**:  
```bash
PASO: 00004 IZQUIERDA: 3 DERECHA: N/A ARRIBA: 3 ABAJO: 1 MOVIMIENTO: ABAJO 
```


### Paso 00005 - FINAL
```
    
    
   C
    
```
En el paso anterior el conejo devoró una zanahoria, pero como ya consumió todas las que debía consumir, el algoritmo termina.

**Se imprime en consola**:  
```bash
PASO: 00005 FINAL
Conejo satisfecho!  
Duracion: 0 h:00 m:00.02 s
```

## Analisis

En base al ejemplo anterior, podemos hacer varias pruebas sobre el algoritmo:



# Algoritmo Genetico

Un algoritmo genético, es una especialización del algoritmo beam search, que se usa para resolver algunos problemas de búsqueda. Este algoritmo está inspirado en la evolución biológica y su base genético-molecular.

El funcionamiento de este es relativamente fácil de entender, se crea o toma una población base, la cual está compuesta de individuos y a su vez cada individuo está compuesto de un conjunto de genes (que en el fondo es un array con determinados valores), luego se seleccionan padres con base a algún criterio y se reproducen, para esto se usan genes del sujeto "padre" y los restantes de la "madre", usando algún tipo de política particular que puede variar de la implementación del mismo posteriormente pueden haber hijos que tengan mutaciones y ellos también ingresan a la población.

Luego de esto basado en el Darwinismo social se crea una función que calcule la aptitud de este sujeto y posteriormente se eliminan de esta generación a los individuos menos aptos, enviando a los mejores a la siguiente generación y repitiendo esto repetidamente hasta encontrar un resultado que cumpla los requisitos, o bien hasta que se cumpla alguna otra condición, sea tiempo o poder computacional.


## Implementación Proyecto Corto 3

Llevando la definición anterior al contexto del proyecto corto número 3 se nos presenta una "matriz" la cual es un tablero que tiene representaciones de un conejo (C) y varias zanahorias (Z), una dirección inicial (hacia donde el conejo se moverá cuando inicie) y el algoritmo se encargará de agregar una serie de direccionadores izquierda (<), derecha (>), arriba (^), abajo (v), además de una dirección inicial implícita; que causarán que el conejo cambie su dirección al caminar sobre ellas, con el objetivo de que se coma cada una , bien la mayoría de las zanahorias.

## Problemas potenciales detectados

A continuación se listan una serie de problemas de implementación encontrados y la solución que se les dio a estos.

### Problema 1: Enciclamientos

Existe posibilidad de que el conejo después de colocar una serie de direccionadores empiece a "correr en círculos", las 2 posibilidades son:

Enciclamiento Cuadrado/Rectangular

``` python
[['v','C',' ','<'],
 [' ','Z',' ',' '],
 ['>',' ',' ','^'],
 [' ',' ','Z',' '],]
```

Encilamiento en línea recta

``` python
[['>','C',' ','<'],
 [' ','Z',' ',' '],
 [' ',' ',' ',' '],
 [' ',' ','Z',' '],]
```

Este tipo de casos causan que la funcion de aptitud (fitness) se encicle, ya que esta tiene que evaluar la ruta del conejo y esta nunca termina. 

La solcion tomada a esto fue guardar en una tabla un string que tenga la inicial en ingles de la direccion, seguido de la casillaX y posterior la casillaY separada por guiones (esto para evitar ambiguedad), y revisar constantemente la casilla y direccion que tiene el conejo, ejemplo:

``` python
['u0_23','r3_4','d22_4','l1_1']
```


### Problema 2: Direccionador en casilla inicial

Este problema está más sujeto a implementación, interpretabilidad o bien ambigüedad o falta de información en la especificación del proyecto, sea como sea: hay 2 posibles interpretaciones para esto:

1) El conejo cambia su dirección al ingresar a la casilla con direccionador
2) El conejo cambia su dirección al salir de la casilla con direccionador

Para el proyecto se toma la primera interpretación meramente como una decisión de implementación, por lo tanto si hay un direccionador en la casilla de salida el conejo tomara su dirección original hasta encontrarse con un direccionador que cambie su dirección en una casilla que sea distinta de su casilla de salida

## Ejemplo 1
Se corre un ejemplo con los siguientes parámetros

### Parametros:
- dirección inicial = derecha
- individuos = 20
- generaciones = 100
- probabilidad de mutación = 0.2
- política de cruce = "Columnas"


### Parámetros de evolución:
- Premio de completitud = 10000
- Premio por zanahoria = 50
- Pena por movimiento = 1
- Pena por direccionador = 5


### Tablero:
```
 CZ 
    
   Z
```

### Resultado

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_1.png)

Duracion: 0 h:00 m:08.68 s

### Mejor individuo generación 0 a 6
``` python
[[' ', 'C', 'Z', ' '],
 [' ', ' ', ' ', ' '],
 [' ', ' ', ' ', 'Z'],
 [' ', ' ', ' ', ' ']]
```
### Mejor individuo generación 7
``` python
[[' ', 'C', 'Z', 'v'],
 ['v', ' ', ' ', ' '],
 [' ', 'v', ' ', 'Z'],
 [' ', ' ', ' ', ' ']]
```


### Mejor individuo generación 99
``` python
[[' ', 'C', 'Z', 'v'],
['>', ' ', ' ', ' '],
[' ', ' ', ' ', 'Z'],
[' ', ' ', ' ', ' ']]
```
### Analisis
Como se puede apreciar el algoritmo encuentra una solución completa y luego de la generación número 100 mejora el Fitness eliminando un direccionador en comparacion a la solucion encontrada, la posibilidad de encontrar una mejora en una solución es relativamente baja luego de alcanzar la completitud.


## Ejemplo 2

### Parametros:
- dirección inicial = derecha
- individuos = 20
- generaciones = 1000
- probabilidad de mutación = 0.2
- política de cruce = "Columnas"


### Parametros de evolucion:
- Premio de completitud = 10000
- Premio por zanahoria = 50
- Pena por movimiento = 1
- Pena por direccionador = 5


### Tablero:
```
       
CZ ZZ  
   ZZ Z
 Z  Z  
Z     Z
Z  Z  Z
   Z   

```
### Resultado

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_2.png)

### Mejor individuo generacion 0
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', ' '],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
 ```
 ### Mejor individuo generacion 50
``` python
[[' ', ' ', ' ', '>', ' ', '^', '<'],
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['<', '^', 'v', 'Z', 'Z', ' ', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', '<'],
 ['Z', ' ', ' ', 'v', ' ', 'v', 'Z'],
 ['Z', ' ', ' ', 'Z', '>', ' ', 'Z'],
 ['v', ' ', '>', 'Z', ' ', '>', ' ']]
```
 ### Mejor individuo generacion 100

``` python
[['v', ' ', ' ', '>', ' ', '^', '>'], 
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['<', '^', '>', 'Z', 'Z', 'v', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', '<'],
 ['Z', ' ', ' ', 'v', ' ', ' ', 'Z'],
 ['Z', ' ', '<', 'Z', ' ', 'v', 'Z'],
 ['>', ' ', '>', 'Z', ' ', ' ', ' ']]
```

 ### Mejor individuo generacion 400

``` python
[['^', ' ', ' ', ' ', ' ', ' ', '^'], 
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['^', '<', '<', 'Z', 'Z', ' ', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', ' '],
 ['Z', ' ', '^', '^', ' ', '^', 'Z'],
 ['Z', '<', ' ', 'Z', ' ', '<', 'Z'],
 ['>', ' ', ' ', 'Z', '^', ' ', '>']]
```

### Mejor individuo generacion 999
``` python
[[' ', '<', ' ', ' ', '>', ' ', 'v'],
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['v', ' ', '^', 'Z', 'Z', ' ', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', ' '],
 ['Z', '>', '^', '>', ' ', '^', 'Z'],
 ['Z', '>', ' ', 'Z', ' ', ' ', 'Z'],
 ['>', ' ', ' ', 'Z', '^', ' ', '^']]
```

### Analisis
Pese a que dados estos parametros y entradas no se llega a dar una completitud en la busqueda, el algoritmo muestra claramente como con el pasar de las generaciones la calidad de los individuos va mejorando, por lo que se puede concluir que el algoritmo funciona satisfactoriamente ya que busca buenas soluciones con relativo poco poder computacional.


## Ejemplo 3
Se corre un ejemplo con los siguientes parametros

### Parametros:
- direccion inical = derecha
- individuos = 20
- generaciones = 1000
- probabilidad de mutacion = 0.2
- politica de cruce = "Genes"


### Parametros de evolucion:
- Premio de completitud = 10000
- Premio por zanahoria = 50
- Pena por movimiento = 1
- Pena por direccionador = 5


### Tablero:
```
 CZ 
    
   Z
```

### Resultado

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_3.png)

Duracion: 0 h:00 m:08.68 s

### Mejor individuo generacion 0 a 4
``` python
[[' ', 'C', 'Z', ' '],
 [' ', ' ', ' ', ' '],
 [' ', ' ', ' ', 'Z'],
 [' ', ' ', ' ', ' ']]
```
### Mejor individuo generacion 5
``` python
[['>', 'C', 'Z', 'v'],
 ['>', '>', ' ', ' '],
 [' ', '^', '<', 'Z'],
 [' ', '<', ' ', ' ']]
```

### Mejor individuo generacion 99
``` python
[[' ', 'C', 'Z', 'v'],
 ['>', '>', ' ', ' '],
 [' ', ' ', ' ', 'Z'],
 [' ', '<', ' ', ' ']]
```

### Analisis
Como se puede apreciar el algoritmo encuentra una solucion completa en esta ocacion particular se dio un caso donde la solucion perfecta se encontro en el primer caso, pero en particular converge a una solucion mejor mas rapido que la politica por columnas, cabe resaltar que el poder computacional requerido para esta politica es considerablemente mas alto.


## Ejemplo 4

### Parametros:
- direccion inical = derecha
- individuos = 20
- generaciones = 1000
- probabilidad de mutacion = 0.2
- politica de cruce = "Columnas"


### Parametros de evolucion:
- Premio de completitud = 10000
- Premio por zanahoria = 50
- Pena por movimiento = 1
- Pena por direccionador = 5


### Tablero:
```
       
CZ ZZ  
   ZZ Z
 Z  Z  
Z     Z
Z  Z  Z
   Z   

```
### Resultado

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_2.png)

### Mejor individuo generacion 0
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', ' '],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
 ```
 ### Mejor individuo generacion 20
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '], 
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'], 
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'], 
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
```
 ### Mejor individuo generacion 30

``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
```

 ### Mejor individuo generacion 40

``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', '<']]
```

 ### Mejor individuo generacion 50

``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', '^', ' ', '<']]
```

### Mejor individuo generacion 100
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', '^', ' ', '<']]
```

### Mejor individuo generacion 999
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', '^', ' ', '<']]
```

### Analisis
A diferencia de la politica por filas, esta llega a una convergencia muchisimo mas rapida que el anterior pero esta genero un resulta mas ineficiente que el anterior, ya que la mejor aptutid fue muchisimo mas baja


## Analisis General

# Apéndice

## Instalación

## Uso

## Archivos de entrada 


