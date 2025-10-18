import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, bounds):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))  # tamaño ajustable
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bounds = bounds

    def resize_to_cell(self, cell_size, padding=10):
        """Ajusta el sprite al tamaño de la celda."""
        size = cell_size - padding
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def draw(self, surface):
        surface.blit(self.image, self.rect)
