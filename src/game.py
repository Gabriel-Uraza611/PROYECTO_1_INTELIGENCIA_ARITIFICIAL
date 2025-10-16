"""
CLASE PRINCIPAL DEL JUEGO - Controla toda la aplicación
Responsabilidades:
- Manejar la ventana de Pygame
- Controlar el loop principal del juego
- Gestionar eventos (clics, teclas, etc.)
- Coordinar entre la hormiga, el grid y los algoritmos
- Dibujar todo en pantalla
"""
import pygame, sys
from player import Player
from enemy import Enemy
from goal import Goal
from grid import Grid

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Simulador Beam Search")
        pygame.display.set_icon(pygame.image.load("assets/images & sprites/cute_hornet.png"))

        # --- Dimensiones generales ---
        self.WIDTH, self.HEIGHT = 800, 500
        self.ROOT = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        # --- Área de juego (zona interna) ---
        self.GAME_AREA = pygame.Rect(0, 0, 500, 500)
        

        # --- Crear grid lógico ---
        self.grid = Grid(5, 5, 100)#declaraion de filas y columnas

        # --- Crear entidades ---
        self.player = Player(8, 2, "assets/images & sprites/cute_hornet.png", (self.GAME_AREA.width, self.GAME_AREA.height))
        self.goal = Goal(400, 395, "assets/images & sprites/Npc_sherma.jpg", (self.GAME_AREA.width, self.GAME_AREA.height))

        self.enemies = [
            Enemy(200, 200, "assets/images & sprites/cucarron_lanza.png", (self.GAME_AREA.width, self.GAME_AREA.height)),
            Enemy(200, 200, "assets/images & sprites/cucarron.png", (self.GAME_AREA.width, self.GAME_AREA.height)),
            Enemy(200, 200, "assets/images & sprites/campana.png", (self.GAME_AREA.width, self.GAME_AREA.height)),
            Enemy(200, 200, "assets/images & sprites/ganzo.png", (self.GAME_AREA.width, self.GAME_AREA.height)),
            Enemy(200, 200, "assets/images & sprites/cucarron_lanza.png", (self.GAME_AREA.width, self.GAME_AREA.height)),
        ]

        # --- Panel lateral ---
        self.panel_rect = pygame.Rect(self.GAME_AREA.width + 20, 60, 250, 370)

    # =============== EVENTOS =================
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        if self.btn_beam.collidepoint(pos):
            print("Beam Search seleccionado")
        elif self.btn_dynamic.collidepoint(pos):
            print("Dynamic Weighting seleccionado")
        elif self.btn_reiniciar.collidepoint(pos):
            print("Reiniciar")
        elif self.btn_cerrar.collidepoint(pos):
            pygame.quit()
            sys.exit()

    # =============== ACTUALIZACIÓN =================
    def update(self):
        self.player.update()
        self.goal.update()
        for e in self.enemies:
            e.update()

    # =============== DIBUJO =================
    def draw(self):
        self.ROOT.fill((30, 30, 30))
        
        pygame.draw.rect(self.ROOT, (0, 0, 0), self.GAME_AREA, 6)
        pygame.draw.rect(self.ROOT, (255, 255, 255), self.GAME_AREA)

        # Dibujar cuadrícula
        self.grid.draw(self.ROOT, self.GAME_AREA.x, self.GAME_AREA.y)

        # Dibujar objetos
        self.goal.draw(self.ROOT)
        for e in self.enemies:
            e.draw(self.ROOT)
        self.ROOT.blit(self.player.image, (self.GAME_AREA.x + self.player.rect.x, self.GAME_AREA.y + self.player.rect.y))

        # --- Panel lateral ---
        pygame.draw.rect(self.ROOT, (255, 255, 255), self.panel_rect, border_radius=15)

        font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.ROOT.blit(font.render("Opciones de búsqueda", True, (0, 0, 0)), (self.panel_rect.x + 12, self.panel_rect.y + 20))
        self.ROOT.blit(font.render("Acciones", True, (0, 0, 0)), (self.panel_rect.x + 24, self.panel_rect.y + 190))

        # Botones
        font_btn = pygame.font.SysFont("Verdana", 22, bold=True)
        self.btn_beam = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 60, 200, 50)
        self.btn_dynamic = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 120, 200, 50)
        self.btn_reiniciar = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 230, 200, 50)
        self.btn_cerrar = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 290, 200, 50)

        buttons = [self.btn_beam, self.btn_dynamic, self.btn_reiniciar, self.btn_cerrar]
        colors = [(74, 222, 252), (74, 222, 252), (32, 223, 83), (255, 0, 0)]
        texts = ["Beam Search", "Dynamic W.", "Reiniciar", "Cerrar"]

        for b, c, t in zip(buttons, colors, texts):
            pygame.draw.rect(self.ROOT, c, b, border_radius=15)
            self.ROOT.blit(font_btn.render(t, True, (255, 255, 255)), (b.x + 20, b.y + 8))

        pygame.display.update()

    # =============== LOOP =================
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()