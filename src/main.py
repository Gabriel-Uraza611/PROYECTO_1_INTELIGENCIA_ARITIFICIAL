import pygame, sys
from player import Player
from enemy import Enemy
from goal import Goal
pygame.init()
pygame.display.set_caption("Simulador Beam Search")

# Dimensiones
WIDTH, HEIGHT = 800, 600
GAME_AREA = pygame.Rect(0, 0, 500, 600)  #? x, y, ancho, alto, parametros para ventana interna

ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load("assets/images & sprites/cute_hornet.png"))

# Cargar fondo de la "zona de juego"
game_background = pygame.image.load("assets/images & sprites/Foreground.jpg")
game_background = pygame.transform.scale(game_background, (GAME_AREA.width, GAME_AREA.height))

# Crear jugador dentro del área de juego
hornet = Player(GAME_AREA.x + 15, GAME_AREA.y + 15, "assets/images & sprites/cute_hornet.png", (GAME_AREA.width, GAME_AREA.height))
sherma = Goal(405, 485, "assets/images & sprites/Npc_sherma.jpg", (GAME_AREA.width, GAME_AREA.height))

#creacion de enemigos
enemies = [
    Enemy(15, 250, "assets/images & sprites/cucarron_lanza.png", (GAME_AREA.width, GAME_AREA.height)),
    Enemy(115, 370, "assets/images & sprites/cucarron.png", (GAME_AREA.width, GAME_AREA.height)),
    Enemy(120, 130, "assets/images & sprites/campana.png", (GAME_AREA.width, GAME_AREA.height)),
    Enemy(220, 500, "assets/images & sprites/ganzo.png", (GAME_AREA.width, GAME_AREA.height)),
    Enemy(318, 250, "assets/images & sprites/cucarron_lanza.png", (GAME_AREA.width, GAME_AREA.height)),
]


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizacion de objetos en el tablero
    hornet.update()
    sherma.update()
    for enemy in enemies:
        enemy.update()

    # Dibujar
    
    # --- DIBUJAR INTERFAZ PRINCIPAL ---
    ROOT.fill((0, 140, 110))  # fondo gris oscuro general

    # Dibujar "zona de juego"
    ROOT.blit(game_background, GAME_AREA.topleft)

    # Dibujar borde que delimita el área de juego
    pygame.draw.rect(ROOT, (0, 0, 0), GAME_AREA, 6)
    for enemy in enemies:
        enemy.draw(ROOT)
    # Dibujar al jugador en su área
    # (ajustamos su posición relativa al área)
    ROOT.blit(hornet.image, (GAME_AREA.x + hornet.rect.x, GAME_AREA.y + hornet.rect.y))
    sherma.draw(ROOT)

    # Dibujar la zona de controles (derecha)
    pygame.draw.rect(ROOT, (239,239,239), (800, 50, 200, 476), border_radius=10)
    font = pygame.font.SysFont("consolas", 20)
    text = font.render("Opciones de búsqueda:", True, (255, 255, 255))
    ROOT.blit(text, (820, 70))

    pygame.display.update()
    clock.tick(60)
