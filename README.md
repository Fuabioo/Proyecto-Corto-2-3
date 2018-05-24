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
 > + Contexto del problema  
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

# Contexto del problema

Se tiene un conejo que debe comer cierta cantidad de zanahorias en un tablero de dimensiones NxM. En el siguiente proyecto se trabajan dos acercamientos que se le pueden dar al problema de buscar y comer las zanahorias:

+ Un algoritmo A* en el que el conejo se mueve un paso a la vez.
+ Un algoritmo Genético en el que el conejo se mueve indefinidamente hacia una direccion que puede cambiar si se topa un "direccionador".

# Algoritmo A*

El objetivo principal de este algoritmo en este problema es encontrar para cada paso la direccion que cueste menos para llegar a las zanahorias, hasta satisfacer la cantidad especificada de zanahorias. Se define un "paso" como la obtencion de los pesos para los "nodos" en el campo visual especificado para el conejo, claramente si en alguno de estos nodos posee una zanahoria, el conejo prioriza ir a este nodo.

```python
def step(self):
    current_pos = self.enviroment["bunny"]
    costs, next_node = self.get_neighbour_costs()

    best_direction = get_direction(current_pos, next_node)

    if best_direction == self.last:
        self.counter += 1
    if self.counter > 15:
        access = self.graph.neighbors(current_pos)
        access.pop(next_node)
        next_node = access[random.randint(0, len(access)-1)]
        best_direction = get_direction(current_pos, next_node)

    # Move bunny and eat if there is a carrot
    self.enviroment["bunny"] = next_node
    if self.graph.nodes[next_node].consume_carrot():
        self.enviroment["carrot"].remove(next_node)
        self.args.zanahorias -= 1

    costs["MOVIMIENTO"] = best_direction
    return costs
```

La idea principal es que basados en la posicion actual del conejo, se exploran los nodos dentro del campo visual del conejo, al obtener todos los costos como descrito anteriormente entonces se determina la mejor direccion a tomar.

Si se llevan 15 pasos en la misma direccion, se determina que el conejo podria estar enciclado, por lo que decidimos que se cambie la direccion independientemente de los costos con el objetivo de intentar salirse del ciclo. Sin embargo podria darse el caso de que realmente vaya todo bien y se randomiza la direccion, en cuyo caso simplemente el conejo se corrige a si mismo cuando corre el algoritmo en el siguiente paso.

Luego si se pasa sobre una zanahoria, pues el conejo se la come.

Para la implementación del algoritmo, se determina si hay algun nodo en el campo visual del conejo con una zanahoria, de no ser asi pues se randomiza el nodo destino.
```python
for valid_node in accesible_nodes:
    if self.graph.nodes[valid_node].carrot:
        all_costs, next_node = self.get_cost_direction(
            valid_node, accesible_nodes)
        break
if all_costs == {}:
    posibilities = self.graph.neighbors(self.enviroment["bunny"])
    index = random.randint(0, len(posibilities) - 1)
    key = list(posibilities)[index]
    all_costs, next_node = self.get_cost_direction(
        key, accesible_nodes)
```
Una vez decidido el nodo destino, se obtienen los costos y se detemina el nodo con el minimo costo
```python
costs, path = self.a_star_search(node, accesible_nodes)
```
Ya propiamente para la implementación del algoritmo, se define una cola prioritaria para los valores frontera (**frontier**) que se inicializa con el nodo en el que se encuentra el conejo actualmente, luego se van expandiendo los nodos, calculando el costo acumulado para la ruta tomada y el heuristico, y se actualiza el frontier. 
```python
initial = self.enviroment["bunny"]
frontier = PriorityQueue()
frontier.push(element=initial, priority=0)

accumulated_cost = {initial: 0}
paths = {}

result = {}

end = False
while frontier:
    current = frontier.pop()

    if current == goal or end:
        break

    for node in self.graph.neighbors(current):
        if node in accesible_nodes:  # Node in vision field?
            # cost from current to neighbor = 1
            current_cost = accumulated_cost[current] + 1
            if node not in accumulated_cost or current_cost < accumulated_cost[node]:
                accumulated_cost[node] = current_cost
                # f(n) = g(n) + h(n)
                priority = current_cost + heuristic(goal, node)
                result[get_direction(current, node)] = priority
                paths[current] = node
                frontier.push(element=node, priority=priority)
```


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
┌───┬───┬───┬───┐
│   │ C │ Z │   │
├───┼───┼───┼───┤
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │ Z │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
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
┌───┬───┬───┬───┐
│   │   │ C │   │
├───┼───┼───┼───┤
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │ Z │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
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
┌───┬───┬───┬───┐
│   │   │   │ C │
├───┼───┼───┼───┤
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │ Z │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
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
┌───┬───┬───┬───┐
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │ C │
├───┼───┼───┼───┤
│   │   │   │ Z │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
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
┌───┬───┬───┬───┐
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │ C │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
```
En el paso anterior el conejo devoró una zanahoria, pero como ya consumió todas las que debía consumir, el algoritmo termina.

**Se imprime en consola**:  
```bash
PASO: 00005 FINAL
Conejo satisfecho!  
Duracion: 0 h:00 m:00.02 s
```

## Análisis

En base al ejemplo anterior, podemos hacer varias pruebas sobre el algoritmo. Para efectos de pruebas definimos un limite predeterminado de 200 pasos, luego de esta cantidad de pasos el algoritmo se detiene incluso si si no se han consumido las zanahorias requeridas. Notese que esto no quiere decir que no haya solución, mas bien es una decision basada en eficiencia, por lo que se dejo el limite como un parametro mas que se le puede pasar al programa por la consola de comandos.

### Ejecución 1

Se realizo una corrida al algoritmo con un tablero de 25x25 con 50 zanahorias en total, con 10 zanahorias para satisfacer la necesidad del conejo.

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_5.png)

Tal y como se aprecia en la figura, ninguna corrida con los campos de visión alcanzo el limite de pasos.

### Ejecución 2

Se realizo una corrida al algoritmo con un tablero de 25x25 con 100 zanahorias en total, con 10 zanahorias para satisfacer la necesidad del conejo.

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_6.png)

Tal y como se aprecia en la figura, en esta figura tampoco se alcanzo el limite de pasos, se obtuvo siempre la misma cantidad de pasos independientemente de la visión.

### Ejecución 3

Se realizo una corrida al algoritmo con un tablero de 50x50 con 50 zanahorias en total, con 10 zanahorias para satisfacer la necesidad del conejo.

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_7.png)

Se aprecia con facilidad que al ser solamente 50 zanahorias para un espacio de area igual a 2500, se reduce tanto la probabilidad de ver una zanahoria que entre menos visión es mas posible enciclarse buscando.

### Ejecución 4

Se realizo una corrida al algoritmo con un tablero de 50x50 con 100 zanahorias en total, con 10 zanahorias para satisfacer la necesidad del conejo.

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_8.png)

Este caso se asemeja demasiado al anterior, en el sentido de que refleja aun mas el problema de tener zanahorias insuficientemente concentradas y cercanas al conejo. Debido a esto se entra eventualmente en un ciclo infinito.

### Resultados generales

Por lo visto el algoritmo empieza a tener problemas cuando todo el rango de visión es limpiado de zanahorias, por lo que en lo que al conejo respecta, cualquier campo es igual de incierto, haciendolo caer en un ciclo infinito solo terminado por el limite definido.

Como era de esperarse, cada vez que se aumenta el campo de visión la duracion del algorimo aumenta significativamente, por lo que entramos en el dilema "sacrifico tiempo en procesamiento para alcanzar un mayor alcance o sacrifico la completitud para ahorrar tiempo y procesamiento". La linea entre ambas posibilidades es muy clara en todas las ejecuciones presentadas, la linea color rojo resulta ser la mas balanceada en este aspecto. Lo que nos lleva a concluir que para este caso en particular del conejo comiendo zanahorias el valor mas justo para la visión del conejo es 15.

El problema base que se nota en las ejecuciones es que entre mas grande el tablero, mas zanahorias debe tener para evitar perder de vista zanahorias. Esta consideracion va mas orientada hacia el archivo de entrada que al algoritmo en si. Por lo tanto se debe considerar siempre si se desea garantizar completitud del problema evitar casos que lleven a este tipo de ciclos de incertidumbre.

En general, la completitud del problema se ve siempre determinada por la ubicacion de las zanahorias y la posicion inicial del conejo, ademas de si el camino de zanahorias lleva a un dead end, lo cual nos lleva a concluir que no se puede garantizar siempre la completitud de un algoritmo A* con un campo de visión.

# Algoritmo Genético

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

La solcion tomada a esto fue guardar en una tabla un string que tenga la inicial en ingles de la dirección, seguido de la casillaX y posterior la casillaY separada por guiones (esto para evitar ambiguedad), y revisar constantemente la casilla y dirección que tiene el conejo, ejemplo:

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

### Parámetros:
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
┌───┬───┬───┬───┐
│   │ C │ Z │   │
├───┼───┼───┼───┤
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │ Z │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
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
### Análisis
Como se puede apreciar el algoritmo encuentra una solución completa y luego de la generación número 100 mejora el Fitness eliminando un direccionador en comparacion a la solución encontrada, la posibilidad de encontrar una mejora en una solución es relativamente baja luego de alcanzar la completitud.


## Ejemplo 2

### Parámetros:
- dirección inicial = derecha
- individuos = 20
- generaciones = 1000
- probabilidad de mutación = 0.2
- política de cruce = "Columnas"


### Parámetros de evolución:
- Premio de completitud = 10000
- Premio por zanahoria = 50
- Pena por movimiento = 1
- Pena por direccionador = 5


### Tablero:
```
┌───┬───┬───┬───┬───┬───┬───┐
│   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│ C │ Z │   │ Z │ Z │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ Z │ Z │   │ Z │
├───┼───┼───┼───┼───┼───┼───┤
│   │ Z │   │   │ Z │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│ Z │   │   │   │   │   │ Z │
├───┼───┼───┼───┼───┼───┼───┤
│ Z │   │   │ Z │   │   │ Z │
├───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ Z │   │   │   │
└───┴───┴───┴───┴───┴───┴───┘
```
### Resultado

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_2.png)

### Mejor individuo generación 0
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', ' '],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
 ```
 ### Mejor individuo generación 50
``` python
[[' ', ' ', ' ', '>', ' ', '^', '<'],
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['<', '^', 'v', 'Z', 'Z', ' ', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', '<'],
 ['Z', ' ', ' ', 'v', ' ', 'v', 'Z'],
 ['Z', ' ', ' ', 'Z', '>', ' ', 'Z'],
 ['v', ' ', '>', 'Z', ' ', '>', ' ']]
```
 ### Mejor individuo generación 100

``` python
[['v', ' ', ' ', '>', ' ', '^', '>'], 
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['<', '^', '>', 'Z', 'Z', 'v', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', '<'],
 ['Z', ' ', ' ', 'v', ' ', ' ', 'Z'],
 ['Z', ' ', '<', 'Z', ' ', 'v', 'Z'],
 ['>', ' ', '>', 'Z', ' ', ' ', ' ']]
```

 ### Mejor individuo generación 400

``` python
[['^', ' ', ' ', ' ', ' ', ' ', '^'], 
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['^', '<', '<', 'Z', 'Z', ' ', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', ' '],
 ['Z', ' ', '^', '^', ' ', '^', 'Z'],
 ['Z', '<', ' ', 'Z', ' ', '<', 'Z'],
 ['>', ' ', ' ', 'Z', '^', ' ', '>']]
```

### Mejor individuo generación 999
``` python
[[' ', '<', ' ', ' ', '>', ' ', 'v'],
 ['C', 'Z', ' ', 'Z', 'Z', 'v', ' '],
 ['v', ' ', '^', 'Z', 'Z', ' ', 'Z'],
 ['v', 'Z', ' ', ' ', 'Z', '<', ' '],
 ['Z', '>', '^', '>', ' ', '^', 'Z'],
 ['Z', '>', ' ', 'Z', ' ', ' ', 'Z'],
 ['>', ' ', ' ', 'Z', '^', ' ', '^']]
```

### Análisis
Pese a que dados estos parametros y entradas no se llega a dar una completitud en la busqueda, el algoritmo muestra claramente como con el pasar de las generaciones la calidad de los individuos va mejorando, por lo que se puede concluir que el algoritmo funciona satisfactoriamente ya que busca buenas soluciónes con relativo poco poder computacional.


## Ejemplo 3
Se corre un ejemplo con los siguientes parametros

### Parámetros:
- direccion inical = derecha
- individuos = 20
- generaciones = 1000
- probabilidad de mutacion = 0.2
- politica de cruce = "Genes"


### Parámetros de evolución:
- Premio de completitud = 10000
- Premio por zanahoria = 50
- Pena por movimiento = 1
- Pena por direccionador = 5


### Tablero:
```
┌───┬───┬───┬───┐
│   │ C │ Z │   │
├───┼───┼───┼───┤
│   │   │   │   │
├───┼───┼───┼───┤
│   │   │   │ Z │
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
```

### Resultado

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_3.png)

Duracion: 0 h:00 m:08.68 s

### Mejor individuo generación 0 a 4
``` python
[[' ', 'C', 'Z', ' '],
 [' ', ' ', ' ', ' '],
 [' ', ' ', ' ', 'Z'],
 [' ', ' ', ' ', ' ']]
```
### Mejor individuo generación 5
``` python
[['>', 'C', 'Z', 'v'],
 ['>', '>', ' ', ' '],
 [' ', '^', '<', 'Z'],
 [' ', '<', ' ', ' ']]
```

### Mejor individuo generación 99
``` python
[[' ', 'C', 'Z', 'v'],
 ['>', '>', ' ', ' '],
 [' ', ' ', ' ', 'Z'],
 [' ', '<', ' ', ' ']]
```

### Análisis
Como se puede apreciar el algoritmo encuentra una solución completa en esta ocacion particular se dio un caso donde la solución perfecta se encontró en el primer caso, pero en particular converge a una solución mejor mas rápido que la política por columnas, cabe resaltar que el poder computacional requerido para esta política es considerablemente más alto.


## Ejemplo 4

### Parámetros:
- direccion inical = derecha
- individuos = 20
- generaciones = 1000
- probabilidad de mutacion = 0.2
- política de cruce = "Columnas"


### Parámetros de evolución:
- Premio de completitud = 10000
- Premio por zanahoria = 50
- Pena por movimiento = 1
- Pena por direccionador = 5


### Tablero:
```
┌───┬───┬───┬───┬───┬───┬───┐
│   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│ C │ Z │   │ Z │ Z │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ Z │ Z │   │ Z │
├───┼───┼───┼───┼───┼───┼───┤
│   │ Z │   │   │ Z │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│ Z │   │   │   │   │   │ Z │
├───┼───┼───┼───┼───┼───┼───┤
│ Z │   │   │ Z │   │   │ Z │
├───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ Z │   │   │   │
└───┴───┴───┴───┴───┴───┴───┘
```
### Resultado

![alt text](https://github.com/Fuabioo/Proyecto-Corto-2-3/blob/master/addons/Figure_2.png)

### Mejor individuo generación 0
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', ' '],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
 ```
 ### Mejor individuo generación 20
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '], 
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'], 
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'], 
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
```
 ### Mejor individuo generación 30

``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', ' ']]
```

 ### Mejor individuo generación 40

``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', ' ', ' ', '<']]
```

 ### Mejor individuo generación 50

``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', '^', ' ', '<']]
```

### Mejor individuo generación 100
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', '^', ' ', '<']]
```

### Mejor individuo generación 999
``` python
[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
 ['C', 'Z', ' ', 'Z', 'Z', ' ', 'v'],
 [' ', ' ', ' ', 'Z', 'Z', ' ', 'Z'],
 [' ', 'Z', ' ', ' ', 'Z', ' ', ' '],
 ['Z', ' ', ' ', ' ', ' ', ' ', 'Z'],
 ['Z', ' ', ' ', 'Z', ' ', ' ', 'Z'],
 [' ', ' ', ' ', 'Z', '^', ' ', '<']]
```

### Análisis
A diferencia de la política por filas, esta llega a una convergencia muchísimo mas rapida que el anterior pero esta genero un resulta mas ineficiente que el anterior, ya que la mejor aptutid fue muchísimo mas baja


# Análisis sobre políticas de cruce

## Política de filas/columnas

Esta política toma aleatoriamente un porcentaje de filas de un individuo padre y el restante de un individuo madre, de manera que los hijos tienen una herencia mas fuerte de los padres, ya que esta toma algo similar a fragmentos de ADN, lo cual hace que los rasgos de sus padres prevalezcan. Esta funcion genera una convergencia lenta, pero por lo general preseta aptitudes mas altas y es considerablemente mas rapida, esto ultimo puede deberse a efectos de implementación.

## Política de genes

Esta política toma aleatoriamente genes de su padre o madre, lo cual puede hacer que sis hijos difieran de sus padres directos y genera una mayor variabilidad a corto plazo de los individuos. Esta funcion genera una convergencia mas rapida que la anterior, pero sus aptitudes son mas bajas, esto puede ser por efectos de implementación, ademas tiene una complejidad computacion mas alta.


# Apéndice

## Instalación

**Opción #1:**

```bash
python setup.py sdist
python -m pip install dist/tec-2.X.tar.gz
```

**Opción #2:**

```bash
python setup.py install
```

## Uso

**Argumentos A\***

| Parametro | Valor valido | Predeterminado |
| ---: | :--- | :---: |
| tablero-inicial | string: nombre de los archivos | `N/A` |
| vision | número entero mayor a 0 | `2` |
| zanahorias | número entero mayor a 0 | `10` |
| limite | número entero mayor a 0 | `200` |

| Bandera | Predeterminado |
| ---: | :---: |
| a-estrella | `False` |
| debug | `False` |


**Argumentos Genético**

| Parametro | Valor valido | Predeterminado |
| ---: | :--- | :---: |
| individuos | número entero mayor a 0 | `3` |
| generaciones | número entero mayor a 0 | `1000` |
| taza-mutacion | punto flotante mayor a 0 | `0.5` |
| politica | string: gen/row | `gen` |

| Bandera | Predeterminado |
| ---: | :---: |
| genetico | `False` |
| derecha | `False` |
| izquierda | `False` |
| abajo | `False` |
| arriba | `False` |
| debug | `False` |
| show-graphic | `False` |
| guardar-archivos | `True` |

**Estructura de codigo**

Para ejecutar el predictor de votaciones se debe utilizar la siguiente estructura en cualquier programa de python:
```python
# importar el modulo
from tec.ic.ia.pc2 import g08
# ejecutar el algoritmo
g08.main()
```

**Ejemplo**

Considerando que un archivo python `ejemplo.py` tenga la estructura anterior y que lo que queremos es correr un algoritmo A\*:

```bash
python ejemplo.py --tablero-inicial entrada.txt --a-estrella --vision 5 --zanahorias 2
```

Considerando que un archivo python `ejemplo.py` tenga la estructura anterior y que lo que queremos es correr un algoritmo genético:

```bash
python ejemplo.py --tablero-inicial entrada.txt --genetico --derecha --individuos 3 --generaciones 1000
```
Tambien se puede especificar la taza de mutacion y la política de cruces:
```bash
python ejemplo.py --tablero-inicial entrada.txt --genetico --derecha --individuos 3 --generaciones 1000 --taza-mutacion 0.4 --politica row
```


## Archivos de entrada 

Los archivos de entrada pueden ser un tablero cuadrado o rectangular, con los siguientes caracteres:

| Caracter | Descripcion |
| :---: | :--- |
| `C` | Indica la posicion inicial del conejo |
| `Z` | Indica posicion de zanahoria |
| Espacio en blanco | Posicion vacia en el tablero |
| `\n` | Indica el final de una fila |

## Repositorio de proyectos anteriores

[Proyecto Prediccion de Votos](https://github.com/Fuabioo/Proyecto-1---Predicci-n-Votaciones)