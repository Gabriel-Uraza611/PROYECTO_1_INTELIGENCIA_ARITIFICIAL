import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, bounds):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 110))  # tamaño ajustable
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bounds = bounds

    def update(self):
        pass  # La meta normalmente no se mueve

    def draw(self, surface):
        surface.blit(self.image, self.rect)
