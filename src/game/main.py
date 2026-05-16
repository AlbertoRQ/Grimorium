"""Punto de entrada del juego grande.

Mas adelante puedes ejecutar este archivo con:
`py -m game.main`
si trabajas desde la carpeta `src`.
"""

from game.core.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
