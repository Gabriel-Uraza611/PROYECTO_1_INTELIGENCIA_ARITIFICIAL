"""Juego de demostración de algoritmos de búsqueda con IA - Beam Search y Dynamic Weighting.

Este módulo implementa un juego interactivo que muestra el funcionamiento de dos
algoritmos de búsqueda pathfinding en inteligencia artificial:
- Beam Search: Algoritmo de búsqueda heurística que explora los caminos más prometedores
- Dynamic Weighting: Algoritmo que ajusta pesos dinámicamente durante la búsqueda

El juego presenta una cuadrícula navegable donde el jugador puede:
- Generar laberintos aleatorios con obstáculos
- Visualizar el proceso de búsqueda de caminos en tiempo real
- Comparar el rendimiento de diferentes algoritmos de IA
- Interactuar con una interfaz gráfica intuitiva

Características principales:
    - Generación procedural de mapas con distancia mínima entre inicio y meta
    - Visualización paso a paso de los algoritmos de búsqueda
    - Sistema de sonido y efectos visuales
    - Interfaz de usuario con panel de control lateral
    - Redimensionado dinámico de la cuadrícula (2x2 hasta 16x16)

Componentes clave:
    - Game: Clase principal que gestiona el bucle del juego y la lógica
    - Player: Representa al jugador/agente que busca el camino
    - Entity: Gestiona enemigos y objetivos
    - Grid: Maneja la cuadrícula lógica y visual del juego

Uso:
    Ejecutar este archivo directamente para iniciar la demostración:
    >>> python game.py
"""

import sys
import random
import tkinter as tk
from tkinter import messagebox

import pygame

from player import Player
from entity import Entity
from grid import Grid
from algorithms import beam_search, dynamic_weighting_search


class Game:
    """Clase principal que gestiona el bucle del juego y la lógica central.
    
    Coordina todos los componentes del juego: interfaz gráfica, entidades,
    algoritmos de búsqueda, sistema de audio y gestión de estados.
    Implementa el patrón MVC (Modelo-Vista-Controlador) para el juego.

    Atributos:
        WIDTH, HEIGHT (int): Dimensiones de la ventana principal.
        ROOT (pygame.Surface): Superficie principal de renderizado.
        GAME_AREA (pygame.Rect): Área rectangular del tablero de juego.
        grid (Grid): Instancia de la cuadrícula del juego.
        player (Player): Instancia del jugador principal.
        goal (Entity): Entidad objetivo a alcanzar.
        enemies (list): Lista de entidades enemigas.
    
    Métodos:
        spawn_random_positions(count=None): Genera posiciones aleatorias.
        handle_events(): Gestiona eventos de entrada del usuario.
        update(): Actualiza el estado del juego cada frame.
        draw(): Renderiza todos los elementos gráficos.
        run(): Ejecuta el bucle principal del juego.
        handle_goal_reached(): Maneja la lógica al alcanzar la meta.
        redefine_grid(): Redimensiona la cuadrícula según entrada.
    """
    def __init__(self):
        #general
        pygame.init()  # pylint: disable=no-member
        pygame.mixer.init()
        pygame.display.set_caption("BeamSearch & DynamicWeighting")
        pygame.display.set_icon(pygame.image.load("assets/images & sprites/logo.png"))

        #MUSIQUITA
        pygame.mixer.music.load("assets/audio/OST.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        #MUSIQUITA JUEGO ALCANZADO
        self.goal_sound = pygame.mixer.Sound("assets/audio/get_goal_sfx.mp3")
        self.goal_sound.set_volume(0.2)
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
            s.set_volume(0.1)

        # --- Dimensiones generales ---
        self.width, self.height= 1024, 576
        self.root = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("assets/images & sprites/backstage.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.clock = pygame.time.Clock()

        # --- Área de juego (zona interna) ---
        self.game_area = pygame.Rect(120, 38, 500, 500)

        # --- Crear grid lógico (por defecto 8x8) ---
        self.grid = Grid(8, 8, self.game_area.width, self.game_area.height)
        self.last_path = []  # Para guardar la última ruta encontrada

        # --- Guardar referencia a la clase Enemy para crear instancias ---
        self.enemy_class = Entity

        # --- Crear entidades fijas (player y goal) ---
        # NOTA: player se colocará correctamente en spawn_random_positions()
        self.player = Player(10, 3, "assets/images & sprites/cute_hornet.png",
        (self.game_area.x, self.game_area.y, self.game_area.width, self.game_area.height))

        self.goal = Entity(400, 395, "assets/images & sprites/Seek_Quest_Icon.png",
                        (self.game_area.width, self.game_area.height))

        # --- Enemies list vacía inicialmente; serán generados aleatoriamente ---
        self.enemies = []

        # --- Panel lateral ---
        self.panel_rect = pygame.Rect(self.game_area.width + 190, 110, 250, 300)

        # --- Generar enemigos aleatorios (solo al iniciar) ---
        self.spawn_random_positions()

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
        self.btn_mute = pygame.Rect(self.width - 55, self.height - 45, 50, 40)  # tamaño 40x40 px
        self.muted = False  # estado de la música

    # ----------------- método para crear botones -----------------
    def _create_buttons(self):
        self.btn_beam = pygame.Rect(self.panel_rect.x + 10, self.panel_rect.y + 60, 110, 40)
        self.btn_dynamic = pygame.Rect(self.panel_rect.x + 128, self.panel_rect.y + 60, 110, 40)
        self.btn_redefinir = pygame.Rect(self.panel_rect.x + 120, self.panel_rect.y + 188, 90, 40)
        self.btn_reiniciar = pygame.Rect(self.panel_rect.x + 30, self.panel_rect.y +  188, 80, 40)
        self.btn_cerrar = pygame.Rect(self.panel_rect.x + 70, self.panel_rect.y + 310, 90, 40)
        self.btn_reiniciar_ruta = pygame.Rect(
            self.panel_rect.x + 30,
            self.panel_rect.y + 235,
            180,
            40
        )

    #  METODOS GENERALES
    def handle_goal_reached(self):
        """Gestiona las acciones cuando el jugador alcanza la meta.

        Pausa la música, reproduce el sonido de meta alcanzada,
        marca la celda de la meta y programa la reanudación de la música.
        """
        if not self.goal_reached:
            self.goal_reached = True
            print("Meta alcanzada")

            # --- pausar la música de fondo ---
            pygame.mixer.music.pause()

            # --- reproducir sonido corto de meta alcanzada ---
            self.goal_sound.play()

            # --- marcar celda verde ---
            self.goal_highlight = self.goal_cell

            # --- esperar un instante y reanudar música ---
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # pylint: disable=no-member

    @staticmethod
    def get_min_distance(
        rows,
        cols
        ):
        """Calcula la distancia mínima recomendada entre el jugador 
        y la meta según el tamaño de la grid.

        Args:
        rows (int): Número de filas de la grid.
        cols (int): Número de columnas de la grid.

        Returns:
        int: Distancia mínima sugerida.
        """
        # mínimo entre filas y columnas para determinar escala
        size = min(rows, cols)
        if size <= 3:
            return 1  # 3x3 → al menos 1 celda de separación
        elif size == 4:
            return 2  # 4x4 → 2 celdas de separación
        else:
            return size // 2  # matrices grandes → al menos la mitad de la dimensión

    def redefine_grid(self):
        """Redefine el tamaño de la grid según el valor ingresado."""
        if not self.user_text:
            return
        try:
            size = int(self.user_text)
            # --- validar rango permitido ---
            if size < 2 or size > 16:
                # crear ventana tkinter temporal para mostrar warning
                root = tk.Tk()
                root.withdraw()  # oculta ventana principal
                messagebox.showwarning("Tamaño inválido",
                                    "No puedes generar matrices menores a 2x2 ni mayores a 16x16")
                root.destroy()
                return

            # recrear la grid
            self.grid = Grid(size, size, self.game_area.width, self.game_area.height)
            # regenerar enemigos y reposicionar
            self.spawn_random_positions()
            print(f"Grid redefinida a {size}x{size}")

            # --- limpiar y desactivar input ---
            self.user_text = ""
            self.input_active = False
            self.input_color = self.input_color_inactive

        except ValueError:
            pass

    def spawn_random_positions(self, count=None):
        """Genera posiciones aleatorias para player, goal y enemigos,
        asegurando distancia mínima entre player y goal y caminos con obstáculos."""

        self.grid.clear_enemies()
        self.enemies = []

        # --- Player --- (obtenemos celda aleatoria)
        player_cell = self.grid.get_random_empty_cell()
        if not player_cell:
            # fallback: esquina (0,0)
            player_cell = (0, 0)
        self.grid.set_cell(*player_cell, 0)  # opcional, marcar como ocupado

        # --- Meta (Goal) con distancia mínima ---
        min_distance = max(1, self.grid.rows // 2)  # distancia mínima aproximada

        valid_goal_cells = []
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                dist = abs(r - player_cell[0]) + abs(c - player_cell[1])  # Manhattan
                if dist >= min_distance:
                    valid_goal_cells.append((r, c))

        if not valid_goal_cells:
            # fallback en esquina opuesta si no hay celdas válidas
            goal_cell = (self.grid.rows - 1, self.grid.cols - 1)
        else:
            goal_cell = random.choice(valid_goal_cells)

        self.grid.set_cell(*goal_cell, 0)
        self.goal_cell = goal_cell

        # --- Cantidad de enemigos ---
        if count is None:
            if self.grid.rows <= 2 or self.grid.cols <= 2:
                count = 1
            else:
                count = min(self.grid.rows, self.grid.cols)

        # --- Enemies ---
        player_r, player_c = player_cell
        goal_r, goal_c = goal_cell

        direct_path = []
        r_step = 1 if goal_r >= player_r else -1
        c_step = 1 if goal_c >= player_c else -1

        for r in range(player_r, goal_r + r_step, r_step):
            for c in range(player_c, goal_c + c_step, c_step):
                if 0 <= r < self.grid.rows and 0 <= c < self.grid.cols:
                    direct_path.append((r, c))

        enemy_positions = set()
        for _ in range(count):
            pos = self.grid.get_random_empty_cell()
            if direct_path and random.random() < 0.5:
                pos = random.choice(direct_path)

            while pos in (player_cell, goal_cell) or pos in enemy_positions:
                pos = self.grid.get_random_empty_cell()
                if not pos:
                    break
            if not pos:
                break

            r, c = pos
            self.grid.set_cell(r, c, 2)
            enemy_positions.add((r, c))

            enemy_x = self.game_area.x + c * self.grid.cell_size + 5
            enemy_y = self.game_area.y + r * self.grid.cell_size + 5

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
                                (self.game_area.width, self.game_area.height))
            e.resize_to_cell(self.grid.cell_size)
            self.enemies.append(e)

        # --- Ajustar player ---
        player_x = self.game_area.x + player_cell[1] * self.grid.cell_size + 5
        player_y = self.game_area.y + player_cell[0] * self.grid.cell_size + 5
        self.player.rect.topleft = (player_x, player_y)
        self.player.resize_to_cell(self.grid.cell_size)

        # --- Ajustar goal ---
        goal_x = self.game_area.x + goal_cell[1] * self.grid.cell_size + 5
        goal_y = self.game_area.y + goal_cell[0] * self.grid.cell_size + 5
        self.goal.rect.topleft = (goal_x, goal_y)
        self.goal.resize_to_cell(self.grid.cell_size)

        # --- Asignar referencias necesarias al player para modo automático ---
        # Aseguramos que player tenga la referencia a la grid y la meta (tu Player debe usar estas)
        self.player.grid = self.grid
        self.player.cell_size = self.grid.cell_size
        self.player.goal = self.goal_cell
        # limpiar ruta previa (si existía)
        self.player.path = []
        self.player.path_index = 0
        self.player.automatic_mode = False

        # --- Reset flags ---
        self.goal_highlight = None
        self.goal_reached = False

    def reset_positions(self):
        """Coloca player y goal en los extremos del grid."""
        # esquina superior izquierda (fila 0, col 0)
        player_x = self.game_area.x + 0 * self.grid.cell_size + 5
        player_y = self.game_area.y + 0 * self.grid.cell_size + 5

        # esquina inferior derecha (última celda)
        goal_x = self.game_area.x + (self.grid.cols - 1) * self.grid.cell_size + 5
        goal_y = self.game_area.y + (self.grid.rows - 1) * self.grid.cell_size  + 5

        # mover entidades
        self.player.rect.topleft = (player_x, player_y)
        self.goal.rect.topleft = (goal_x, goal_y)

    # =============== EVENTOS ===============
    def handle_events(self):
        """Gestiona todos los eventos de entrada del usuario.

        Procesa eventos de teclado, ratón y temporizador, incluyendo cierre de ventana,
        interacción con botones, entrada de texto y control de la música.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # pylint: disable=no-member
                pygame.quit()  # pylint: disable=no-member
                sys.exit()
            # --- evento para reanudar música ---
            if event.type == pygame.USEREVENT + 1: # pylint: disable=no-member
                pygame.mixer.music.unpause()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0) # pylint: disable=no-member # desactiva el timer
            if event.type == pygame.MOUSEBUTTONDOWN: # pylint: disable=no-member
                # activar o desactivar input box
                if self.input_box.collidepoint(event.pos):
                    self.input_active = not self.input_active
                else:
                    self.input_active = False

                if self.input_active:
                    self.input_color = self.input_color_active
                else:
                    self.input_color = self.input_color_inactive

                # manejo de botones
                self.handle_click(event.pos)
            if event.type == pygame.KEYDOWN and self.input_active: # pylint: disable=no-member
                if event.key == pygame.K_RETURN: # pylint: disable=no-member
                    self.redefine_grid()
                elif event.key == pygame.K_BACKSPACE: # pylint: disable=no-member
                    self.user_text = self.user_text[:-1]
                elif event.unicode.isdigit() and len(self.user_text) < 2:  # máximo 2 dígitos
                    self.user_text += event.unicode

    def handle_click(self, pos):
        """Gestiona las acciones asociadas a los botones del panel lateral y la cuadrícula.

        Según el botón presionado, ejecuta el algoritmo de búsqueda seleccionado,
        reinicia enemigos, redefine el tamaño de la grid, silencia la música,
        cierra el juego o reinicia la ruta actual.
    
        Args:
            pos (tuple): Posición (x, y) del clic del usuario.
        """
        if self.btn_beam.collidepoint(pos):
            random.choice(self.button_sfx).play()
            print("Beam Search seleccionado")
            player_row = (self.player.rect.y - self.game_area.y) // self.grid.cell_size
            player_col = (self.player.rect.x - self.game_area.x) // self.grid.cell_size
            start = (player_row, player_col)
            goal = self.goal_cell
            matrix = [
                [1 if self.grid.get_cell(r, c) == 2 else 0 for c in range(self.grid.cols)]
                for r in range(self.grid.rows)
            ]
            player_x, player_y = self.player.rect.topleft
            start_col = (player_x - self.game_area.x) // self.grid.cell_size
            start_row = (player_y - self.game_area.y) // self.grid.cell_size
            self.start_pos = (start_row, start_col) # pylint: disable=attribute-defined-outside-init

            path = beam_search(matrix, start, goal)

            if path:
                print("Camino encontrado:", path)
                self.last_path = path
                for (r, c) in path:
                    px = self.game_area.x + c * self.grid.cell_size + 5
                    py = self.game_area.y + r * self.grid.cell_size + 5
                    self.player.rect.topleft = (px, py)
                    self.draw()
                    pygame.time.wait(200)
                self.handle_goal_reached()
            else:
                print("no se encontro camino")
        elif self.btn_dynamic.collidepoint(pos):
            random.choice(self.button_sfx).play()
            print("Dynamic Weighting seleccionado")
            player_row = (self.player.rect.y - self.game_area.y) // self.grid.cell_size
            player_col = (self.player.rect.x - self.game_area.x) // self.grid.cell_size
            start = (player_row, player_col)
            goal = self.goal_cell

        # --- construir el mapa lógico (1 = obstáculo, 0 = libre) ---
            matrix = [[1 if self.grid.get_cell(r, c) == 2 else 0
                    for c in range(self.grid.cols)]
                    for r in range(self.grid.rows)]
            player_x, player_y = self.player.rect.topleft
            start_col = (player_x - self.game_area.x) // self.grid.cell_size
            start_row = (player_y - self.game_area.y) // self.grid.cell_size
            self.start_pos = (start_row, start_col)  # pylint: disable=attribute-defined-outside-init

            path = dynamic_weighting_search(matrix, start, goal)

            if path:
                print("Camino encontrado:", path)
                self.last_path = path
                for (r, c) in path:
                    px = self.game_area.x + c * self.grid.cell_size + 5
                    py = self.game_area.y + r * self.grid.cell_size + 5
                    self.player.rect.topleft = (px, py)
                    self.draw()
                    pygame.time.wait(200)
                self.handle_goal_reached()
            else:
                print("No se encontró camino ")
        elif self.btn_reiniciar.collidepoint(pos):
            print("Reiniciar - reubicando enemigos")
            # detener movimiento automático antes de reubicar
            self.player.automatic_mode = False
            self.spawn_random_positions()   # <-- solo cuando el usuario lo pide
        elif self.btn_redefinir.collidepoint(pos):
            print("Redefinir - cambiando tamaño de grid")
            # detener movimiento automático ya que grid cambiará
            self.player.automatic_mode = False
            self.redefine_grid()
        elif self.btn_mute.collidepoint(pos):
            self.toggle_mute()
        elif self.btn_cerrar.collidepoint(pos):
            pygame.quit() # pylint: disable=no-member
            sys.exit()
        elif self.btn_reiniciar_ruta.collidepoint(pos):
            print("Reiniciar solo la ruta actual")
            self.last_path = []
            self.goal_reached = False
            if hasattr(self, "start_pos"):
                start_row, start_col = self.start_pos
            else:
                start_row, start_col = (0, 0)
            self.player.rect.topleft = (
                self.game_area.x + start_col * self.grid.cell_size + 5,
                self.game_area.y + start_row * self.grid.cell_size + 5
            )

    def toggle_mute(self):
        """Activa o desactiva el estado de silencio de la música."""
        if self.muted:
            pygame.mixer.music.set_volume(0.5)  # reactivar volumen
            self.muted = False
        else:
            pygame.mixer.music.set_volume(0)    # silenciar
            self.muted = True

    # =============== ACTUALIZACIÓN =================
    def update(self):
        """Actualiza el estado de todas las entidades del juego y verifica si se alcanzó la meta."""
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
        """Dibuja todos los elementos gráficos del juego en la ventana principal.

        Renderiza el área de juego, la cuadrícula, el jugador, la meta, los enemigos,
        los caminos, el panel lateral, los botones y los campos de entrada.
        """
        #COLORES
        white = (255, 255, 255)
        black = (0, 0, 0)
        color_player = (244, 213, 0)   # amarillo
        color_enemy = (255, 0, 0)      # rojo
        color_goal = (0, 0, 255)       # azul
        color_goal_reached = (0, 255, 0)  # verde

        # fondo global
        self.root.blit(self.background, (0, 0))

        # área de juego
        pygame.draw.rect(self.root, white, self.game_area)

        #grid
        self.grid.draw(self.root, self.game_area.x, self.game_area.y)
        # --- Dibujar la última ruta encontrada ---
        if self.last_path:
            color_path = (0, 255, 0)
            for (r, c) in self.last_path:
                pygame.draw.rect(
                    self.root,
                    color_path,
                    pygame.Rect(
                        self.game_area.x + c * self.grid.cell_size + 3,
                        self.game_area.y + r * self.grid.cell_size + 3,
                        self.grid.cell_size - 6,
                        self.grid.cell_size - 6
                    )
                )
        padding = 2  # margen dentro de la celda

        # --- Player --- (dibujamos la celda en la que está)
        player_row = (self.player.rect.y - self.game_area.y) // self.grid.cell_size
        player_col = (self.player.rect.x - self.game_area.x) // self.grid.cell_size
        pygame.draw.rect(self.root, color_player,
                        pygame.Rect(self.game_area.x + player_col * self.grid.cell_size + padding,
                                    self.game_area.y + player_row * self.grid.cell_size + padding,
                                    self.grid.cell_size - 2*padding,
                                    self.grid.cell_size - 2*padding))
        pygame.draw.rect(self.root, black,
                        pygame.Rect(self.game_area.x + player_col * self.grid.cell_size,
                                    self.game_area.y + player_row * self.grid.cell_size,
                                    self.grid.cell_size,
                                    self.grid.cell_size), 2)

        # --- Colorear casilla de la meta ---
        goal_row, goal_col = self.goal_cell
        goal_color = color_goal_reached if self.goal_reached else color_goal
        pygame.draw.rect(self.root, goal_color,
                        pygame.Rect(self.game_area.x + goal_col * self.grid.cell_size + padding,
                                    self.game_area.y + goal_row * self.grid.cell_size + padding,
                                    self.grid.cell_size - 2*padding,
                                    self.grid.cell_size - 2*padding))
        # borde negro de la meta
        pygame.draw.rect(self.root, black,
                        pygame.Rect(self.game_area.x + goal_col * self.grid.cell_size,
                                    self.game_area.y + goal_row * self.grid.cell_size,
                                    self.grid.cell_size, self.grid.cell_size), 2)

        # --- Enemigos ---
        for enemy in self.enemies:
            enemy_row = (enemy.rect.y - self.game_area.y) // self.grid.cell_size
            enemy_col = (enemy.rect.x - self.game_area.x) // self.grid.cell_size
            pygame.draw.rect(self.root, color_enemy,
                pygame.Rect(self.game_area.x + enemy_col * self.grid.cell_size + padding,
                            self.game_area.y + enemy_row * self.grid.cell_size + padding,
                            self.grid.cell_size - 2*padding,
                            self.grid.cell_size - 2*padding))
            pygame.draw.rect(self.root, black,
                pygame.Rect(self.game_area.x + enemy_col * self.grid.cell_size,
                            self.game_area.y + enemy_row * self.grid.cell_size,
                            self.grid.cell_size,
                            self.grid.cell_size), 2)

        #borde game area
        pygame.draw.rect(self.root, black, self.game_area, 6)

        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(self.root)

        # Dibujar objetivo y jugador
        self.goal.draw(self.root)
        self.root.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        # Panel lateral y botones
        # Crear una superficie semitransparente para el panel
        pygame.draw.rect(self.root, (161, 240, 206), self.panel_rect, border_radius=15)

        font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.root.blit(font.render("Opciones de búsqueda", True, (0, 0, 0)),
                    (self.panel_rect.x + 12, self.panel_rect.y + 20))

        # dibujar botones
        font_btn = pygame.font.SysFont("Verdana", 14, bold=True)
        buttons = [self.btn_beam, self.btn_dynamic, self.btn_reiniciar_ruta, self.btn_reiniciar,
                   self.btn_cerrar, self.btn_redefinir]
        colors = [
            (86, 227, 159), (86, 227, 159), (86, 227, 159), (86, 227, 159),
            (239, 111, 108), (86, 227, 159)
            ]  # color botones
        texts = [
            "Beam Search", "Dynamic W.", "Reiniciar Ruta", "Reiniciar",
            "Cerrar", "Redefinir"
            ]

        for b, c, t in zip(buttons, colors, texts):
            pygame.draw.rect(self.root, c, b, border_radius=15)
            text_surf = font_btn.render(t, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=b.center)
            self.root.blit(text_surf, text_rect)

        # --- campo de entrada ---
        pygame.draw.rect(self.root, self.input_color, self.input_box, 2)
        font_input = pygame.font.SysFont("Verdana", 18, bold=True)
        txt_surface = font_input.render(self.user_text, True, (0, 0, 0))
        self.root.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 3))
        self.root.blit(font_input.render("Tamaño:", True, (0, 0, 0)),
                    (self.input_box.x, self.input_box.y - 25))

        # dibujar botón de mute
        color = (200, 0, 0) if self.muted else (0, 200, 0)
        pygame.draw.rect(self.root, color, self.btn_mute, border_radius=5)

        font_small = pygame.font.SysFont("Verdana", 12, bold=True)
        text = "Mute" if not self.muted else "UnMute"
        text_surf = font_small.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.btn_mute.center)
        self.root.blit(text_surf, text_rect)

        pygame.display.update()

# =============== LOOP =================
    def run(self):
        """Ejecuta el bucle principal del juego.

        Atiende eventos, actualiza el estado y dibuja la pantalla a 60 FPS.
        """
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
