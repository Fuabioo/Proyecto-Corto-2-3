# Inteligencia Artificial

Instituto Tecnológico de Costa Rica  
Ingeniería en Computación  
IC6200 - Inteligencia Artificial  
I Semestre, 2018

# Grupo #8

Fabio Mora Cubillo - 2013012801  
Sergio Moya Valerin - 2013015682  
Gabriel Venegas Castro - 2013115967

# Contenidos

Proyecto Corto 2 y 3 - Conejo y Zanahorias
 > + Algoritmo A*  
 > +---- Descripción  
 > +---- Calculo de heuristico  
 > +---- Ejemplo  
 > +---- Analisis  
 > + Algoritmo Genetico 
 > +---- Descripción
 > +---- Problemas potenciales detectados
 > +---- Ejemplo  
 > +---- Analisis  
 > + Apéndice  
 > +---- Instalación  
 > +---- Uso  
 > +---- Archivos de entrada  

# Algoritmo A*

## Calculo de heuristico

La pregunta que uno se debe hacer es como calcular **h**. Tenemos que el conejo tiene vision limitada, por lo que sabemos que tenemos que utilizar un heuristico por aproximacion. Esto nos limita a tres opciones: "Euclidean Distance", "Manhattan Distance", "Diagonal Distance".
Como sabemos que en el algoritmo solo se puede mover el conejo en cuatro direcciones (arriba, abajo, izquierda y derecha) entonces se sabe que para el heuristico se debe utilizar la distancia Manhattan, que consiste en obtener el valor absoluto de las diferencias de las posiciones (x, y) del nodo actual con el nodo destino.

```python
def heuristic(node_1, node_2):
    """ Heuristic when only 4 directions are posible (Manhattan) """
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
Podemos notar que en la posicion derecha al conejo hay una zanahoria, esto implica que el conejo va a querer ir ahi, por lo que ese seria su nodo destino.

| Nodo | Posicion |f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(0, 2)` | `0` |
| Izquierda | `(0, 0)` | `3` |
| Derecha | `(0, 2)` | `1` |
| Abajo | `(1, 1)` | `3` |
| Arriba | `N/A` | `N/A` |

**Decision**: Moverse hacia la derecha  
**Calculos realizados**(directamente impresos por el algoritmo):  
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
En el paso anterior el conejo devoro una zanahoria, por lo que debe buscar ptra. Podemos notar que el conejo puede ver una zanahoria a lo lejos, esto implica que el conejo va a querer ir ahi, por lo que ese seria su nodo destino.

| Nodo | Posicion | f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(0, 2)` | `0` |
| Izquierda | `(0, 1)` | `5` |
| Derecha | `(0, 3)` | `3` |
| Abajo | `(1, 2)` | `5` |
| Arriba | `N/A` | `N/A` |

**Desicion**: Moverse hacia la derecha  
**Calculos realizados**(directamente impresos por el algoritmo):  
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
Como el conejo no ha comido ninguna zanahoria, se continua con la busqueda.

| Nodo | Posicion |f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(0, 3)` | `0` |
| Izquierda |`(0, 2)` | `4` |
| Derecha | `N/A` | `N/A` |
| Abajo | `(1, 3)` | `2` |
| Arriba | `N/A` | `N/A` |

**Desicion**: Moverse hacia la derecha  
**Calculos realizados**(directamente impresos por el algoritmo):  
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
Como el conejo no ha comido ninguna zanahoria, se continua con la busqueda. Al estar la zanahoria en un nodo adyacente, la siguiente accion sera devorarla. 

| Nodo | Posicion |f(n) = g(n) + h(n) |
|:--:|:--:|:--:|
| Conejo | `(1, 3)` | `0` |
| Izquierda | `(1, 2)` | `3` |
| Derecha | `N/A` | `N/A` |
| Abajo | `(2, 3)` | `1` |
| Arriba | `(0, 3)` | `3` |

**Desicion**: Moverse hacia la derecha  
**Calculos realizados**(directamente impresos por el algoritmo):  
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
En el paso anterior el conejo devoro una zanahoria, pero como ya consumio todas las que debia consumir, el algoritmo termina.

**Se imprime en consola**:  
```bash
PASO: 00005 FINAL
Conejo satisfecho!  
Duracion: 0 h:00 m:00.02 s
```

## Analisis

En base al ejemplo anterior, podemos hacer varias pruebas sobre el algoritmo:



# Algoritmo Genetico

Un algoritmo genetico, es una especializacion de el algoritmo beam search, que se usa para resolver algunos problemas de busqueda. Este algoritmo esta inspirado en la evolucion biologica y su base genetico-molecular.

El funcionamiento de este es relativamente facil de entender, se crea o toma una poblacion base, la cual esta compuesta de individuos y a su vez cada individuo esta compuesto de un conjunto de genes (que en el fondo es un array con determinados valores), luego se seleccionan padres con base a algun criterio y se reproducen, para esto se usan genes del sujeto "padre" y los restantes de la "madre", usando algun tipo de politica particular que puede variar de la implementacion del mismo posterior mente pueden haber hijos que tengan mutaciones y ellos tambien ingresan a la poblacion.

Luego de esto basado en el Darwinismo social se crea una funcion que calcule la aptitud de este sujeto y posteriormente se eliminan de esta generacion a los individuos menos aptos, enviando a los mejores a la siguiente generacion y repitiendo esto repetidamente hasta encontrar un resultado que cumpla los requisitos, o bien hasta que se cumpla alguna otra condicion, sea tiempo o poder computacional.


## Implementacion Proyecto Corto 3

LLevando la definiion anterior al contexto del proyecto corto numero 3 se nos presenta una "matriz" la cual es un tablero que tiene representaciones de un conejo (C) y varias zanahorias (Z), una direccion inicial (hacia donde el conejo se movera cuando inicie) y el algoritmo se encargara de agregar una serie de direccionadores izquierda (<), derecha (>), arriba (^), abajo (v), ademas de una direccion inicial implicita; que causaran que el conejo cambie su direccion al caminar sobre ellas, con el objetivo de que se coma cada una , bien la mayoria de las zanahorias.

## Problemas potenciales detectados

A continuacion se listaran una serie de problemas de implementacion encontrados y la solucion que se les dio a estos.

### Problema 1: Enciclamientos

Existe posibilidad de que el conejo despues de colocar una serie de direccionadores empieze a "correr en circulos", las 2 posibilidades son:

Enciclamiento Cuadrado/Rectangular

``` python
[['v','C',' ','<'],
 [' ','Z',' ',' '],
 ['>',' ',' ','^'],
 [' ',' ','Z',' '],]
```

Encilamiento en linea recta

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

Este problema esta mas sujeto a implementacion, interpretabilidad o bien ambiguedad o falta de informacion en la especificacion del proyecto, sea como sea: hay 2 posibles interpretaciones para esto:

1) El conejo cambia su direccion al ingresar a la casilla con direccionador
2) El conejo cambia su direccion al salir de la casilla con direccionador

Para el proyecto se toma la primera interpretacion meramente como una desicion de implementacion, por lo tanto si hay un direccionador en la casilla de salida el conejo tomara su direccion original hasta encontrarse con un direccionador que cambie su direccion en una casilla que sea distinta de su casilla de salida

## Ejemplo
Se corre un ejemplo con los siguientes parametros

### Parametros:
- direccion inical = derecha
- individuos = 20
- generaciones = 100
- probabilidad de mutacion = 0.2
- politica de cruce = "Columnas"


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

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_1.png)

Duracion: 0 h:00 m:08.68 s

### Mejor individuo generacion 1 a 5
``` python
[[' ', 'C', 'Z', ' '],
 [' ', ' ', ' ', ' '],
 [' ', ' ', ' ', 'Z'],
 [' ', ' ', ' ', ' ']]
```
### Mejor individuo generacion 6
``` python
[[' ', 'C', '>Z', 'v'],
 ['^', '^', '^', ' '],
 [' ', ' ', '^', '>Z'],
 ['<', ' ', 'v', 'v']] 
```

  
## Analisis

# Conclusiones


# Apéndice

## Instalación

## Uso

## Archivos de entrada
