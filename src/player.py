import pygame
from algorithms import beam_search

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, bounds, grid=None, goal=None, cell_size=80, beam_width=3):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))  # tamaño inicial

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 5
        self.bounds = bounds  # (x, y, ancho, alto)
        self.move_delay = 100
        self.last_move_time = 0

        
        self.grid = grid
        self.goal = goal
        self.cell_size = cell_size
        self.beam_width = beam_width
        self.path = []
        self.path_index = 0
        self.automatic_mode = False  #controla si se mueve solo

    def resize_to_cell(self, cell_size, padding=10):
        """Ajusta el sprite al tamaño de la celda."""
        size = cell_size - padding
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

   


    def enable_auto_move(self, start_cell, goal_cell):
        """Activa el movimiento automatico usando Beam Search."""
        if self.grid is None or self.goal is None:
            print("No hay grid o meta definida.")
            return

        self.path = beam_search(start_cell, goal_cell, self.grid, beam_width=self.beam_width)
        if self.path:
            self.automatic_mode = True
            self.path_index = 0
            print(f" Camino encontrado ({len(self.path)} pasos).")
        else:
            print(" No se encontro un camino con Beam Search.")

    def move_to_next_cell(self):
        """Mueve al personaje a la siguiente celda con retardo controlado."""
        now = pygame.time.get_ticks()  # tiempo actual en milisegundos
        if self.path_index < len(self.path) and now - self.last_move_time >= self.move_delay:
            cell = self.path[self.path_index]
            self.rect.topleft = (cell[1] * self.cell_size, cell[0] * self.cell_size)
            self.path_index += 1
            self.last_move_time = now
        elif self.path_index >= len(self.path):
            self.automatic_mode = False
            print("Hornet ha llegado a la meta.")

   
   
    def update(self):
        if self.automatic_mode:
            # Movimiento automatico paso a paso
            self.move_to_next_cell()

            #limitar movimiento a los bordes del GAME_AREA
            self.rect.x = max(self.bounds[0], min(self.rect.x, self.bounds[0] + self.bounds[2] - self.rect.width))
            self.rect.y = max(self.bounds[1], min(self.rect.y, self.bounds[1] + self.bounds[3] - self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)