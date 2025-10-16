"""
CLASE PRINCIPAL DEL JUEGO - Controla toda la aplicación
Responsabilidades:
- Manejar la ventana de Pygame
- Controlar el loop principal del juego
- Gestionar eventos (clics, teclas, etc.)
- Coordinar entre la hormiga, el grid y los algoritmos
- Dibujar todo en pantalla
"""
# src/game.py
import pygame, sys
import random
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

        # --- Crear grid lógico (5x5 con celdas de 100 px) ---
        self.grid = Grid(5, 5, 100)

        # --- Guardar referencia a la clase Enemy para crear instancias ---
        self.enemy_class = Enemy

        # --- Crear entidades fijas (player y goal) ---
        # Nota: aquí pasas coordenadas en píxeles a Player/Goal según su constructor actual
        # He puesto posiciones fijas (ajusta si quieres que Player use celdas del grid)
        self.player = Player(10, 3, "assets/images & sprites/cute_hornet.png",
                             (self.GAME_AREA.width, self.GAME_AREA.height))
        self.goal = Goal(400, 395, "assets/images & sprites/Npc_sherma.jpg",
                         (self.GAME_AREA.width, self.GAME_AREA.height))

        # --- Enemies list vacía inicialmente; serán generados aleatoriamente ---
        self.enemies = []

        # --- Panel lateral ---
        self.panel_rect = pygame.Rect(self.GAME_AREA.width + 20, 60, 250, 370)

        # --- Generar enemigos aleatorios (solo al iniciar) ---
        self.spawn_random_enemies()

        # Botones (se definen aquí para que existan antes de handle_click)
        self._create_buttons()

    # ----------------- método para crear botones -----------------
    def _create_buttons(self):
        self.btn_beam = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 60, 200, 50)
        self.btn_dynamic = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 120, 200, 50)
        self.btn_reiniciar = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 230, 200, 50)
        self.btn_cerrar = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 290, 200, 50)

    # ----------------- método que antes estaba anidado: ahora es método de clase -----------------
    def spawn_random_enemies(self, count=5):
        """Genera posiciones aleatorias para los enemigos.
        Coloca marcas en grid.matrix (valor 2) y crea instancias Enemy.
        """
        self.grid.clear_enemies()
        self.enemies = []

        for _ in range(count):
            pos = self.grid.get_random_empty_cell()  # (fila, col)
            if not pos:
                break
            r, c = pos
            # marcar en la matriz lógica
            self.grid.set_cell(r, c, 2)

            # convertir a píxeles (centrar dentro de la celda con un padding)
            enemy_x = self.GAME_AREA.x + c * self.grid.cell_size + 10
            enemy_y = self.GAME_AREA.y + r * self.grid.cell_size

            # crear instancia de Enemy
            image_path = random.choice([
                "assets/images & sprites/cucarron.png",
                "assets/images & sprites/ganzo.png",
                "assets/images & sprites/campana.png",
                "assets/images & sprites/cucarron_lanza.png",
            ])
            e = self.enemy_class(enemy_x, enemy_y, image_path,
                                 (self.GAME_AREA.width, self.GAME_AREA.height))
            self.enemies.append(e)

    # =============== EVENTOS =================
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        # comprobamos botones - reiniciar llamará a spawn_random_enemies
        if self.btn_beam.collidepoint(pos):
            print("Beam Search seleccionado")
        elif self.btn_dynamic.collidepoint(pos):
            print("Dynamic Weighting seleccionado")
        elif self.btn_reiniciar.collidepoint(pos):
            print("Reiniciar - reubicando enemigos")
            self.spawn_random_enemies()   # <-- solo cuando el usuario lo pide
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
        # fondo global
        self.ROOT.fill((30, 30, 30))

        # área de juego (blanco) y su borde
        pygame.draw.rect(self.ROOT, (255, 255, 255), self.GAME_AREA)
        pygame.draw.rect(self.ROOT, (0, 0, 0), self.GAME_AREA, 6)

        # (Opcional) dibujar la cuadrícula lógica si quieres verla:
        self.grid.draw(self.ROOT, self.GAME_AREA.x, self.GAME_AREA.y)

        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(self.ROOT)

        # Dibujar objetivo y jugador (fuera del bucle de enemigos)
        self.goal.draw(self.ROOT)
        self.ROOT.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        # Panel lateral y botones
        pygame.draw.rect(self.ROOT, (255, 255, 255), self.panel_rect, border_radius=15)
        font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.ROOT.blit(font.render("Opciones de búsqueda", True, (0, 0, 0)),
                       (self.panel_rect.x + 12, self.panel_rect.y + 20))
        self.ROOT.blit(font.render("Acciones", True, (0, 0, 0)),
                       (self.panel_rect.x + 24, self.panel_rect.y + 190))

        # dibujar botones
        font_btn = pygame.font.SysFont("Verdana", 22, bold=True)
        buttons = [self.btn_beam, self.btn_dynamic, self.btn_reiniciar, self.btn_cerrar]
        colors = [(74, 222, 252), (74, 222, 252), (32, 223, 83), (255, 0, 0)]
        texts = ["Beam Search", "Dynamic W.", "Reiniciar", "Cerrar"]

        for b, c, t in zip(buttons, colors, texts):
            pygame.draw.rect(self.ROOT, c, b, border_radius=15)
            text_surf = font_btn.render(t, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=b.center)
            self.ROOT.blit(text_surf, text_rect)

        pygame.display.update()

    # =============== LOOP =================
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            # NO llamamos spawn_random_enemies aquí: solo al iniciar o al reiniciar
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
