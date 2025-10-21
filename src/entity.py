"""
Módulo de entidades gráficas para el juego de búsqueda con IA.

Define la clase base Entity que representa cualquier objeto visual en el juego:
enemigos, objetivos y otros elementos interactivos. Proporciona funcionalidades
básicas de renderizado y manipulación de sprites.

Características:
    - Carga y escalado de imágenes con transparencia
    - Ajuste automático al tamaño de celdas del grid
    - Gestión de límites y posicionamiento
    - Sistema de dibujado optimizado para Pygame

Esta clase sirve como base para todos los elementos visuales móviles o estáticos
en la simulación de algoritmos de búsqueda.
"""

import pygame

class Entity(pygame.sprite.Sprite):
    """Representa una entidad gráfica básica en el juego.
    
    Clase base para todos los elementos visuales del juego como
    enemigos, objetivos y otros objetos interactivos. Maneja
    la carga de sprites, posicionamiento y renderizado básico.
    
    Atributos:
        image (Surface): Imagen del sprite con transparencia.
        rect (Rect): Área rectangular que define posición y tamaño.
        bounds (tuple): Límites del área donde puede existir la entidad.
    
    Métodos:
        resize_to_cell(): Ajusta el tamaño al de las celdas del grid.
        draw(): Renderiza la entidad en la superficie especificada.
    """
    def __init__(self, x, y, image_path, bounds):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 110))  # tamaño ajustable
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bounds = bounds

    def resize_to_cell(self, cell_size, padding=10):
        """Ajusta el sprite al tamaño de la celda."""
        size = cell_size - padding
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def draw(self, surface):
        """Dibuja la entidad en la superficie dada."""
        surface.blit(self.image, self.rect)
