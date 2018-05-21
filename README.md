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

Por ejemplo, para el siguiente espacio de 4x4 con 2 zanahorias
```
 CZ 
    
   Z
    
```
Podemos notar que en la posicion derecha al conejo hay una zanahoria, esto implica que el conejo va a querer ir ahi, por lo que ese seria su nodo destino.

| Nodo | Posicion | g(n) | h(n) | f(n) = g(n) + h(n) |
|:--:|:--:|:--:|:--:|:--:|
| Conejo | `(0, 1)` | `0` | `1` | `1` |
| Izquierda | `(0, 0)` | `1` | `2` | `3` |
| Derecha | `(0, 2)` | `1` | `0` | `1` |
| Abajo | `(1, 1)` | `1` | `2` | `0` |
| Arriba | `N/A` | `N/A` | `N/A` | `N/A` |


