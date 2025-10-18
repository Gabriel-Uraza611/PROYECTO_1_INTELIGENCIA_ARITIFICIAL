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
import tkinter as tk
from tkinter import messagebox
from player import Player
from enemy import Enemy
from goal import Goal
from grid import Grid

class Game:
    def __init__(self):
        #general
        pygame.init()
        pygame.mixer.init()
        

        pygame.display.set_caption("BeamSearch & DynamicWeighting")
        pygame.display.set_icon(pygame.image.load("assets/images & sprites/logo.png"))

        #MUSIQUITA
        pygame.mixer.music.load("assets/audio/OST.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        #MUSIQUITA JUEGO ALCANZADO
        self.goal_sound = pygame.mixer.Sound("assets/audio/get_goal_sfx.mp3")
        self.goal_sound.set_volume(0.6)
        self.goal_reached = False
        self.goal_highlight = None

        #sonidos efectos
        self.button_sfx_files = [
            "assets/audio/ADIDOO.wav",
            "assets/audio/CARAMA.wav",
            "assets/audio/HEGALE.wav",
            "assets/audio/SHAW.wav",
            "assets/audio/GIT_GUD.wav"
        ]
        # Convertirlos en objetos Sound
        self.button_sfx = [pygame.mixer.Sound(path) for path in self.button_sfx_files]
        for s in self.button_sfx:
            s.set_volume(0.3)


        # --- Dimensiones generales ---
        self.WIDTH, self.HEIGHT = 1024, 576
        self.ROOT = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = pygame.image.load("assets/images & sprites/backstage.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        # --- Área de juego (zona interna) ---
        self.GAME_AREA = pygame.Rect(120, 38, 500, 500)

        # --- Crear grid lógico (5x5 con celdas de 100 px) ---
        self.grid = Grid(7, 7, self.GAME_AREA.width, self.GAME_AREA.height)

        # --- Guardar referencia a la clase Enemy para crear instancias ---
        self.enemy_class = Enemy

        # --- Crear entidades fijas (player y goal) ---
        # Nota: aquí pasas coordenadas en píxeles a Player/Goal según su constructor actual
        # He puesto posiciones fijas (ajusta si quieres que Player use celdas del grid)
        self.player = Player(10, 3, "assets/images & sprites/cute_hornet.png",
                     (self.GAME_AREA.x, self.GAME_AREA.y, self.GAME_AREA.width, self.GAME_AREA.height))

        self.goal = Goal(400, 395, "assets/images & sprites/Seek_Quest_Icon.png",
                         (self.GAME_AREA.width, self.GAME_AREA.height))

        # --- Enemies list vacía inicialmente; serán generados aleatoriamente ---
        self.enemies = []

        # --- Panel lateral ---
        self.panel_rect = pygame.Rect(self.GAME_AREA.width + 190, 110, 250, 300)

        # --- Generar enemigos aleatorios (solo al iniciar) ---
        self.spawn_random_enemies()

        #--- Resetear las posiciones de meta y player----


        # Botones (se definen aquí para que existan antes de handle_click)
        self._create_buttons()
        self.input_active = False
        self.user_text = ""
        self.input_box = pygame.Rect(self.panel_rect.x + 20, self.panel_rect.y + 142, 200, 30)
        self.input_color_inactive = pygame.Color('lightskyblue3')
        self.input_color_active = pygame.Color('dodgerblue2')
        self.input_color = self.input_color_inactive

        # botón pequeño de mute en la esquina inferior derecha
        self.btn_mute = pygame.Rect(self.WIDTH - 55, self.HEIGHT - 45, 50, 40)  # tamaño 40x40 px
        self.muted = False  # estado de la música

    # ----------------- método para crear botones -----------------
    def _create_buttons(self):
        self.btn_beam = pygame.Rect(self.panel_rect.x + 10, self.panel_rect.y + 60, 110, 40)
        self.btn_dynamic = pygame.Rect(self.panel_rect.x + 128, self.panel_rect.y + 60, 110, 40)
        self.btn_redefinir = pygame.Rect(self.panel_rect.x + 120, self.panel_rect.y + 188, 90, 40)
        self.btn_reiniciar = pygame.Rect(self.panel_rect.x + 30, self.panel_rect.y +  188, 80, 40)
        self.btn_cerrar = pygame.Rect(self.panel_rect.x + 70, self.panel_rect.y + 235, 90, 40)

    # ----------------- método que antes estaba anidado: ahora es método de clase -----------------
    def spawn_random_enemies(self, count=None):
        """Genera enemigos según el tamaño del grid."""
        self.grid.clear_enemies()
        self.enemies = []

        # --- calcular cantidad de enemigos según tamaño ---
        if count is None:
            # regla: si el grid es menor o igual a 2x2 → 1 enemigo
            if self.grid.rows <= 2 or self.grid.cols <= 2:
                count = 1
            else:
                # usa el menor de los dos tamaños (más equilibrado)
                count = min(self.grid.rows, self.grid.cols)

        # coordenadas reservadas (player y goal)
        player_cell = (0, 0)
        goal_cell = (self.grid.rows - 1, self.grid.cols - 1)

        # --- generar enemigos ---
        for _ in range(count):
            pos = self.grid.get_random_empty_cell()
            while pos in (player_cell, goal_cell):
                pos = self.grid.get_random_empty_cell()
                if not pos:
                    break
            if not pos:
                break

            r, c = pos
            self.grid.set_cell(r, c, 2)

            enemy_x = self.GAME_AREA.x + c * self.grid.cell_size + 10
            enemy_y = self.GAME_AREA.y + r * self.grid.cell_size

            image_path = random.choice([
                "assets/images & sprites/B_Flintstone_Flyer.png",
                "assets/images & sprites/B_Pilgrim_Groveller.png",
                "assets/images & sprites/B_Pilgrim_Pouncer.png",
                "assets/images & sprites/B_Skarr_Scout.png",
                "assets/images & sprites/B_Smelt_Shoveller.png",
                "assets/images & sprites/B_Winged_Pilgrim.png",
                "assets/images & sprites/Mossgrub.png",
                "assets/images & sprites/Mossmir.png",
                "assets/images & sprites/Skarrlid.png",
                "assets/images & sprites/Skarrwing.png",
                "assets/images & sprites/B_Caranid.png",
                "assets/images & sprites/B_Beastfly.png",
                "assets/images & sprites/B_Skull_Scuttler.png",
                "assets/images & sprites/B_Pilgrim_Hiker.png",
            ])

            e = self.enemy_class(enemy_x, enemy_y, image_path,
                                (self.GAME_AREA.width, self.GAME_AREA.height))
            e.resize_to_cell(self.grid.cell_size)  # <-- adapta sprite
            self.enemies.append(e)

            # redefinir los tamaños
            self.player.resize_to_cell(self.grid.cell_size)
            self.goal.resize_to_cell(self.grid.cell_size)

            for e in self.enemies:
                e.resize_to_cell(self.grid.cell_size)

            self.reset_positions()
            self.goal_highlight = None
            self.goal_reached = False


    
    def reset_positions(self):
        """Coloca player y goal en los extremos del grid."""
        # esquina superior izquierda (fila 0, col 0)
        player_x = self.GAME_AREA.x + 0 * self.grid.cell_size + 5
        player_y = self.GAME_AREA.y + 0 * self.grid.cell_size + 5

        # esquina inferior derecha (última celda)
        goal_x = self.GAME_AREA.x + (self.grid.cols - 1) * self.grid.cell_size + 5
        goal_y = self.GAME_AREA.y + (self.grid.rows - 1) * self.grid.cell_size  + 5

        # mover entidades
        self.player.rect.topleft = (player_x, player_y)
        self.goal.rect.topleft = (goal_x, goal_y)
    
    def redefinir_grid(self):
        """Redefine el tamaño de la grid según el valor ingresado."""
        if not self.user_text:
            return
        try:
            size = int(self.user_text)
            # --- validar rango permitido ---
            if size < 2 or size > 12:
                # crear ventana tkinter temporal para mostrar warning
                root = tk.Tk()
                root.withdraw()  # oculta ventana principal
                messagebox.showwarning("Tamaño inválido",
                                    "No puedes generar matrices menores a 2x2 ni mayores a 12x12")
                root.destroy()
                return

            # recrear la grid
            self.grid = Grid(size, size, self.GAME_AREA.width, self.GAME_AREA.height)
            # regenerar enemigos y reposicionar
            self.spawn_random_enemies()
            print(f"Grid redefinida a {size}x{size}")

            # --- limpiar y desactivar input ---
            self.user_text = ""
            self.input_active = False
            self.input_color = self.input_color_inactive

        except ValueError:
            pass

    def toggle_mute(self):
        if self.muted:
            pygame.mixer.music.set_volume(0.5)  # reactivar volumen
            self.muted = False
        else:
            pygame.mixer.music.set_volume(0)    # silenciar
            self.muted = True
    
    def handle_goal_reached(self):
        if not self.goal_reached:
            self.goal_reached = True
            print("Meta alcanzada") 

            # --- pausar la música de fondo ---
            pygame.mixer.music.pause()

            # --- reproducir sonido corto de meta alcanzada ---
            self.goal_sound.play()

            # --- marcar celda verde ---
            self.goal_highlight = (self.grid.rows - 1, self.grid.cols - 1)

            # --- esperar un instante y reanudar música ---
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # 1000 ms = 1 seg

    # =============== EVENTOS =================
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             # --- evento para reanudar música ---
            if event.type == pygame.USEREVENT + 1:
                pygame.mixer.music.unpause()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # desactiva el timer
            if event.type == pygame.MOUSEBUTTONDOWN:
                # activar o desactivar input box
                if self.input_box.collidepoint(event.pos):
                    self.input_active = not self.input_active
                else:
                    self.input_active = False
                self.input_color = self.input_color_active if self.input_active else self.input_color_inactive

                # manejo de botones
                self.handle_click(event.pos)

            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    self.redefinir_grid()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.unicode.isdigit() and len(self.user_text) < 2:  # máximo 2 dígitos
                    self.user_text += event.unicode


    def handle_click(self, pos):
        # comprobamos botones - reiniciar llamará a spawn_random_enemies -------------> OJO BORRAR PRINTS CUANDO SE TERMINE EL PROYECTO
        if self.btn_beam.collidepoint(pos):
            random.choice(self.button_sfx).play()
            print("Beam Search seleccionado")
        elif self.btn_dynamic.collidepoint(pos):
            random.choice(self.button_sfx).play()
            print("Dynamic Weighting seleccionado")
        elif self.btn_reiniciar.collidepoint(pos):
            print("Reiniciar - reubicando enemigos")
            self.spawn_random_enemies()   # <-- solo cuando el usuario lo pide
        elif self.btn_redefinir.collidepoint(pos):
            print("Redefinir - cambiando tamaño de grid")
            self.redefinir_grid()
        elif self.btn_mute.collidepoint(pos):
            self.toggle_mute()
        elif self.btn_cerrar.collidepoint(pos):
            pygame.quit()
            sys.exit()

    # =============== ACTUALIZACIÓN =================
    def update(self):
        self.player.update()
        self.goal.update()
        for e in self.enemies:
            e.update()
        # Detectar si el jugador alcanzó la meta (solo una vez)
        if not self.goal_reached and self.player.rect.colliderect(self.goal.rect):
            self.handle_goal_reached()
            self.goal_reached = True


    # =============== DIBUJO =================
    def draw(self):
        # fondo global
        self.ROOT.blit(self.background, (0, 0))

        # área de juego (blanco) y su borde
        pygame.draw.rect(self.ROOT, (255, 255, 255), self.GAME_AREA)
        pygame.draw.rect(self.ROOT, (0, 0, 0), self.GAME_AREA, 6)


        # dibujar la grid (usa offsets como ya lo haces)
        self.grid.draw(self.ROOT, self.GAME_AREA.x, self.GAME_AREA.y)
        # Si la meta fue alcanzada, pinta la celda de verde
        if self.goal_highlight:
            r, c = self.goal_highlight
            rect = pygame.Rect(
                self.GAME_AREA.x + c * self.grid.cell_size,
                self.GAME_AREA.y + r * self.grid.cell_size,
                self.grid.cell_size,
                self.grid.cell_size
            )
            pygame.draw.rect(self.ROOT, (0, 255, 0), rect)  # verde fuerte
            pygame.draw.rect(self.ROOT, (0, 0, 0), rect, 2)  # borde negro opcional


        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(self.ROOT)

        # Dibujar objetivo y jugador (fuera del bucle de enemigos)
        self.goal.draw(self.ROOT)
        self.ROOT.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        # Panel lateral y botones
        # Crear una superficie semitransparente para el panel
        pygame.draw.rect(self.ROOT, (161, 240, 206), self.panel_rect, border_radius=15)

        font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.ROOT.blit(font.render("Opciones de búsqueda", True, (0, 0, 0)),
                       (self.panel_rect.x + 12, self.panel_rect.y + 20))
        

        # dibujar botones
        font_btn = pygame.font.SysFont("Verdana", 14, bold=True)
        buttons = [self.btn_beam, self.btn_dynamic, self.btn_reiniciar, self.btn_cerrar, self.btn_redefinir]
        colors = [(86, 227, 159), (86, 227, 159), (86, 227, 159), (239, 111, 108), (86, 227, 159)] #COLOR BOTONES
        texts = ["Beam Search", "Dynamic W.", "Reiniciar", "Cerrar", "Redefinir"]

        for b, c, t in zip(buttons, colors, texts):
            pygame.draw.rect(self.ROOT, c, b, border_radius=15)
            text_surf = font_btn.render(t, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=b.center)
            self.ROOT.blit(text_surf, text_rect)
        
                # --- campo de entrada ---
        pygame.draw.rect(self.ROOT, self.input_color, self.input_box, 2)
        font_input = pygame.font.SysFont("Verdana", 18, bold=True)
        txt_surface = font_input.render(self.user_text, True, (0, 0, 0))
        self.ROOT.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 3))
        self.ROOT.blit(font_input.render("Tamaño:", True, (0, 0, 0)), (self.input_box.x, self.input_box.y - 25))

        # dibujar botón de mute
        color = (200, 0, 0) if self.muted else (0, 200, 0)
        pygame.draw.rect(self.ROOT, color, self.btn_mute, border_radius=5)

        # opcional: poner texto o icono
        font_small = pygame.font.SysFont("Verdana", 12, bold=True)
        text = "Mute" if not self.muted else "UnMute"
        text_surf = font_small.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.btn_mute.center)
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
