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

class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]  # 0 = vacío

    def set_cell(self, r, c, value):
        self.matrix[r][c] = value

    def get_cell(self, r, c):
        return self.matrix[r][c]

    def draw(self, surface, offset_x=0, offset_y=0):
        # Dibujar líneas de cuadrícula
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(
                    offset_x + c * self.cell_size,
                    offset_y + r * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(surface, (60, 60, 60), rect, 1)
