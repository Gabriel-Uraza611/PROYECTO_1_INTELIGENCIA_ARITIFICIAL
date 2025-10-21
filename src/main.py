"""
Punto de entrada principal del juego de demostración de algoritmos IA.

Este módulo minimalista inicia la aplicación ejecutando el bucle principal
del juego. Su función exclusiva es crear una instancia de Game y ejecutarla.

Uso:
    Ejecutar este archivo directamente para lanzar la aplicación:
    >>> python main.py
    o
    >>> python -m main

Mantiene una separación clara entre la inicialización y la lógica del juego,
permitiendo un fácil mantenimiento y posibles extensiones futuras.
"""

from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()