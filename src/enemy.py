import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, bounds):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))  # tamaño ajustable
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bounds = bounds

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)
