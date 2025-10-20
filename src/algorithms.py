"""
ALGORITMOS DE BÚSQUEDA - El cerebro del proyecto
Responsabilidades:
- BEAM SEARCH: Encontrar camino limitando nodos por nivel
- DYNAMIC WEIGHTING: Ajustar peso de heurística dinámicamente
- Calcular f(n) = g(n) + h(n) + ε * (1 - (d(n)/N)) * h(n)
- Devolver el camino óptimo para la hormiga
"""
import heapq
import math

def heuristic(a, b):
    """Distancia Manhattan."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def beam_search(matrix, start, goal, beam_width=3):
    """
    Implementación de Beam Search.
    - matrix: matriz 2D (0 = libre, 1 = obstáculo)
    - start: tupla (fila, col)
    - goal: tupla (fila, col)
    - beam_width: número máximo de nodos a explorar por nivel
    """
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4 direcciones cardinales

    # Cada elemento del beam: (heuristic + costo acumulado, posición actual, camino recorrido)
    beam = [(heuristic(start, goal), start, [start])]
    visited = set([start])

    while beam:
        new_beam = []

        # Expandir cada nodo en el beam actual
        for _, current, path in beam:
            if current == goal:
                return path  # ¡Camino encontrado!

            for dr, dc in directions:
                nr, nc = current[0] + dr, current[1] + dc
                neighbor = (nr, nc)
                if (
                    0 <= nr < rows and 0 <= nc < cols and
                    matrix[nr][nc] == 0 and
                    neighbor not in visited
                ):
                    visited.add(neighbor)
                    new_cost = len(path) + heuristic(neighbor, goal)
                    new_beam.append((new_cost, neighbor, path + [neighbor]))

        # Si no hay más nodos que expandir, detener
        if not new_beam:
            break

        # Ordenar por el costo total (heurística + profundidad)
        new_beam.sort(key=lambda x: x[0])

        # Mantener solo los mejores beam_width nodos
        beam = new_beam[:beam_width]

    return None  # Si no se encontró camino