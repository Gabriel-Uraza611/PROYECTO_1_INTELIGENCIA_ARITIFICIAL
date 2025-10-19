"""
ALGORITMOS DE BÚSQUEDA - El cerebro del proyecto
Responsabilidades:
- BEAM SEARCH: Encontrar camino limitando nodos por nivel
- DYNAMIC WEIGHTING: Ajustar peso de heurística dinámicamente
- Calcular f(n) = g(n) + h(n) + ε * (1 - (d(n)/N)) * h(n)
- Devolver el camino óptimo para la hormiga
"""
def manhattan(a, b):
    """Distancia Manhattan entre dos celdas (tuplas (fila, columna))"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def beam_search(start, goal, grid_obj, beam_width=3):
    """
    Implementación de Beam Search adaptada al objeto Grid.
    - grid_obj: instancia de la clase Grid (con .rows, .cols y .matrix)
    - start, goal: tuplas (fila, columna)
    - beam_width: cantidad máxima de nodos por nivel
    """
    # Extraemos la matriz interna de la Grid (suponiendo que tiene atributo .matrix)
    matrix = getattr(grid_obj, "matrix", None)
    if matrix is None:
        raise ValueError("El objeto Grid no tiene atributo 'matrix' (asegúrate de implementarlo).")

    def get_neighbors(pos):
        (x, y) = pos
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        result = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_obj.rows and 0 <= ny < grid_obj.cols:
                # 0 = libre, 2 = enemigo (obstáculo)
                if matrix[nx][ny] != 2:
                    result.append((nx, ny))
        return result

    frontier = [(start, [start])]
    explored = set()

    while frontier:
        # ordenar por heurística y mantener los mejores β
        frontier = sorted(frontier, key=lambda x: manhattan(x[0], goal))[:beam_width]
        new_frontier = []

        for node, path in frontier:
            if node == goal:
                return path  # camino encontrado

            explored.add(node)
            for neighbor in get_neighbors(node):
                if neighbor not in explored:
                    new_frontier.append((neighbor, path + [neighbor]))

        frontier = new_frontier

    return None  # no se encontró camino
