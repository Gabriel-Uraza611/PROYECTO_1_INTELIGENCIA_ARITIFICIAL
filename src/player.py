import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, bounds):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))  # ancho, alto en píxeles

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 5
        self.bounds = bounds  # (ancho, alto) de la ventana

    def resize_to_cell(self, cell_size, padding=10):
        """Ajusta el sprite al tamaño de la celda."""
        size = cell_size - padding
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        # Limitar movimiento a los bordes de la pantalla
        self.rect.x = max(0, min(self.rect.x, self.bounds[0] - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.bounds[1] - self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

