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


#? creacion de panel de control de acciones



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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_beam.collidepoint(event.pos):
                print("Beam Search seleccionado")
            elif btn_dynamic.collidepoint(event.pos):
                print("Dynamic Weighting seleccionado")
            elif btn_reiniciar.collidepoint(event.pos):
                print("Reiniciar")
            elif btn_cerrar.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    # Actualizacion de objetos en el tablero
    hornet.update()
    sherma.update()
    for enemy in enemies:
        enemy.update()

    # Dibujar
    
    # --- DIBUJAR INTERFAZ PRINCIPAL ---
    ROOT.fill((0, 140, 255))  # fondo 

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

     #Panel de acciones

    PANEL_X = GAME_AREA.width + 20  # deja un pequeño margen
    PANEL_Y = 50
    PANEL_WIDTH = 250
    PANEL_HEIGHT = 500

    panel_rect = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)

    panel_color = (255, 255, 255)  
    pygame.draw.rect(ROOT, panel_color, panel_rect, border_radius=15)

    # Dibujar la zona de controles (derecha)

    font = pygame.font.SysFont("Verdana", 18, bold=True)
    text1 = font.render("Opciones de búsqueda", True, (0, 0, 0))
    ROOT.blit(text1, (panel_rect.x + 12, panel_rect.y + 20))


    text2 = font.render("Acciones", True, (0, 0, 0))
    ROOT.blit(text2, (panel_rect.x + 70, panel_rect.y + 190))

    
    #Botones simples
    font_btn = pygame.font.SysFont("Verdana", 22, bold=True)

    # Definir botones como rectángulos
    btn_beam = pygame.Rect(panel_rect.x + 20, panel_rect.y + 60, 200, 50)
    btn_dynamic = pygame.Rect(panel_rect.x + 20, panel_rect.y + 120, 200, 50)
    btn_reiniciar = pygame.Rect(panel_rect.x + 20, panel_rect.y + 230, 200, 50)
    btn_cerrar = pygame.Rect(panel_rect.x + 20, panel_rect.y + 290, 200, 50)

    # Dibujar botones
    button_colors = [(74, 222, 252), (74, 222, 252), (32, 223, 83), (255, 0, 0)]
    buttons = [btn_beam, btn_dynamic, btn_reiniciar, btn_cerrar]
    button_texts = ["Beam Search", "Dynamic W.", "Reiniciar", "Cerrar"]

    for b, c, t in zip(buttons, button_colors, button_texts):
        pygame.draw.rect(ROOT, c, b, border_radius=15)
        ROOT.blit(font_btn.render(t, True, (255, 255, 255)), (b.x + 20, b.y + 8))

    pygame.display.update()
    clock.tick(60)
