"""
Módulo de algoritmos de búsqueda pathfinding para inteligencia artificial.

Implementa dos algoritmos de búsqueda heurística utilizados en el juego
para encontrar caminos óptimos en entornos con obstáculos:

Algoritmos implementados:
    - Beam Search: Algoritmo que limita la exploración a los nodos más prometedores
        en cada nivel, balanceando eficiencia y optimalidad
    - Dynamic Weighting Search: Variante de A* que ajusta dinámicamente el peso
        de la heurística basado en el progreso hacia el objetivo

Funciones principales:
    - beam_search(): Encuentra caminos limitando la amplitud de búsqueda
    - dynamic_weighting_search(): Ajusta pesos heurísticos durante la exploración
    - heuristic(): Calcula distancia Manhattan entre dos puntos

Estos algoritmos forman el núcleo de la IA del juego, permitiendo la navegación
autónoma del jugador a través de laberintos generados proceduralmente.
"""
import heapq

def heuristic(a, b):
    """Calcula la distancia Manhattan entre dos puntos.
    
    Args:
        a (tuple): Coordenadas del primer punto (fila, columna).
        b (tuple): Coordenadas del segundo punto (fila, columna).
    
    Returns:
        int: Distancia Manhattan entre los puntos a y b.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def beam_search(matrix, start, goal, beam_width=3):
    """Implementa el algoritmo Beam Search para pathfinding.
    
    Encuentra un camino desde el punto inicial al objetivo explorando
    solo los nodos más prometedores en cada nivel, utilizando una
    búsqueda heurística con amplitud limitada.
    
    Args:
        matrix (list): Matriz 2D donde 0=libre, 1=obstáculo.
        start (tuple): Coordenadas de inicio (fila, columna).
        goal (tuple): Coordenadas del objetivo (fila, columna).
        beam_width (int): Número máximo de nodos por nivel (default: 3).
    
    Returns:
        list or None: Lista de coordenadas del camino encontrado 
                    o None si no hay camino posible.
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

#Dynamic Weighting
def dynamic_weighting_search(matrix, start, goal):
    """Implementa búsqueda con pesos dinámicos tipo A* mejorado.
    
    Variante de A* que ajusta dinámicamente el peso de la heurística
    basándose en el progreso hacia el objetivo, mejorando la eficiencia
    en entornos complejos.
    
    Args:
        matrix (list): Matriz 2D donde 0=libre, 1=obstáculo.
        start (tuple): Coordenadas de inicio (fila, columna).
        goal (tuple): Coordenadas del objetivo (fila, columna).
    
    Returns:
        list or None: Camino encontrado como lista de coordenadas
                    o None si no existe camino.
    """
    rows, cols = len(matrix), len(matrix[0])

    # 8 direcciones posibles (N, S, E, O)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}

    # factor de peso dinámico (va cambiando según la distancia)
    base_weight = 1.5

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            # reconstruir camino
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] == 0:
                new_cost = g_score[current] + 1

                if (nr, nc) not in g_score or new_cost < g_score[(nr, nc)]:
                    g_score[(nr, nc)] = new_cost

                    # Ajusta peso dinámicamente según progreso hacia la meta
                    dist_to_goal = heuristic((nr, nc), goal)
                    total_dist = heuristic(start, goal)
                    progress = 1 - (dist_to_goal / (total_dist + 1e-5))
                    dynamic_weight = base_weight + progress  # aumenta conforme se acerca

                    f_score = new_cost + dynamic_weight * heuristic((nr, nc), goal)
                    heapq.heappush(open_list, (f_score, (nr, nc)))
                    came_from[(nr, nc)] = current

    return None  # si no hay camino
