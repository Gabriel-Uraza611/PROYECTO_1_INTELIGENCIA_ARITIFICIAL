import pygame
from algorithms import beam_search
import threading
import tkinter as tk
from tkinter import messagebox
from algorithms import beam_search, dynamic_weighting_search

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

        self.path = beam_search(self.grid.matrix, start_cell, goal_cell, beam_width=self.beam_width)
        if self.path:
            self.automatic_mode = True
            self.path_index = 0
            print(f" Camino encontrado ({len(self.path)} pasos).")
            
            def mostrar_popup():
                root = tk.Tk()
                root.withdraw()
                ruta_texto = " → ".join([f"({r},{c})" for r, c in self.path])
                messagebox.showinfo("Ruta encontrada", f"Camino de la hormiga:\n\n{ruta_texto}")
                root.destroy()
            threading.Thread(target=mostrar_popup, daemon=True).start()
            

        else:
            print(" No se encontro un camino con Beam Search.")


    def draw(self, surface):
        surface.blit(self.image, self.rect)