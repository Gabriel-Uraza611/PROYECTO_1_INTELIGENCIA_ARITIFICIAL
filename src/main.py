import pygame
import sys

"""
ARCHIVO PRINCIPAL - Punto de entrada del programa
Aquí solo se inicializa el juego y se ejecuta el loop principal
NO poner lógica de juego aquí, solo el inicio
"""


#?inicializacion de la ventana
pygame.init()

ROOT = pygame.display.set_mode((1024,576))


#* COLORES:

BLANCO = (230,230,230)

ROOT.fill(BLANCO)
pygame.display.set_caption(title="Hornet vs hormigas")
icono = pygame.image.load("src/cute_hornet.png")
pygame.display.set_icon(icono)

#?bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()