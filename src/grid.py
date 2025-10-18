"""
CLASE DEL TABLERO/MATRIZ - Representa el mundo de la hormiga
Responsabilidades:
- Crear y mantener la matriz de celdas
- Saber qué hay en cada posición (vacío, veneno, hongo)
- Validar movimientos (qué posiciones puede visitar la hormiga)
- Dibujar el grid en pantalla
- Gestionar la colocación de elementos (venenos/hongos)
"""

# src/grid.py
import pygame
import random

class Grid:
    def __init__(self, rows, cols, area_width, area_height):
        self.rows = rows
        self.cols = cols
        # calcular cell_size automáticamente
        self.cell_size = min(area_width // cols, area_height // rows)
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        
    def set_cell(self, r, c, value):
        self.matrix[r][c] = value

    def get_cell(self, r, c):
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
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(
                    offset_x + c * self.cell_size,
                    offset_y + r * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(surface, (60, 60, 60), rect, 1)
