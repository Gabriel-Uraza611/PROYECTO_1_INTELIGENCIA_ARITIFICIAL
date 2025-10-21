"""
Módulo de gestión de cuadrícula para el entorno de búsqueda.

Representa el mundo navegable donde ocurre la búsqueda pathfinding. Maneja
la estructura lógica y visual del tablero, incluyendo obstáculos, áreas
transitables y validación de movimientos.

Responsabilidades:
    - Crear y mantener la matriz lógica del entorno
    - Gestionar tipos de celdas (vacías, obstáculos, objetivos)
    - Proporcionar utilidades para generación procedural
    - Renderizar la cuadrícula visualmente
    - Ofrecer métodos para acceso y modificación del estado del grid

La clase Grid es fundamental para la representación espacial que los algoritmos
de IA utilizan para planificar caminos y tomar decisiones.
"""

# src/grid.py
import random
import pygame

class Grid:

    """Gestiona la cuadrícula lógica y visual del entorno de juego.
    
    Representa el mundo navegable donde los algoritmos de búsqueda operan.
    Maneja la matriz de celdas, validación de posiciones y renderizado
    del tablero visual.
    
    Atributos:
        rows (int): Número de filas en la cuadrícula.
        cols (int): Número de columnas en la cuadrícula.
        cell_size (int): Tamaño en píxeles de cada celda.
        matrix (list): Matriz 2D que representa el estado de cada celda.
    
    Métodos:
        set_cell(r, c, value): Establece el valor de una celda específica.
        get_cell(r, c): Obtiene el valor de una celda específica.
        clear_enemies(): Elimina todos los enemigos del grid.
        get_random_empty_cell(): Devuelve una celda vacía aleatoria.
        draw(surface, offset_x, offset_y): Dibuja la cuadrícula en pantalla.
    """

    def __init__(self, rows, cols, area_width, area_height):
        self.rows = rows
        self.cols = cols
        # calcular cell_size automáticamente
        self.cell_size = min(area_width // cols, area_height // rows)
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    def set_cell(self, r, c, value):
        """Establece el valor de una celda específica en la matriz."""
        self.matrix[r][c] = value

    def get_cell(self, r, c):
        """Obtiene el valor de una celda específica en la matriz."""
        return self.matrix[r][c]

    def clear_enemies(self):
        """Elimina solo las celdas que contienen enemigos (valor 2)."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.matrix[r][c] == 2:
                    self.matrix[r][c] = 0

    def get_random_empty_cell(self):
        """Devuelve una celda vacía al azar (fila, col)."""
        empty_cells = [(r, c) for r in range(self.rows)
                        for c in range(self.cols) if self.matrix[r][c] == 0]
        return random.choice(empty_cells) if empty_cells else None

    def draw(self, surface, offset_x=0, offset_y=0):
        """Dibuja la cuadrícula en la superficie dada.

        Args:
            surface (pygame.Surface): Superficie donde se dibuja la cuadrícula.
            offset_x (int): Desplazamiento horizontal en píxeles.
            offset_y (int): Desplazamiento vertical en píxeles.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(
                    offset_x + c * self.cell_size,
                    offset_y + r * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(surface, (60, 60, 60), rect, 1)
