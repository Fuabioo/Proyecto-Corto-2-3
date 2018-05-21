# Proyecto-Corto-2-3

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


