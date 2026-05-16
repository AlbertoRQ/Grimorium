"""Clase base para todas las pantallas.

La idea es que todas las pantallas compartan la misma forma:
- reaccionar a eventos
- actualizarse
- dibujarse
"""


class BaseScreen:
    def __init__(self, game):
        # Guardamos el objeto principal del juego para acceder
        # a pantalla, reloj, cambio de pantalla, etc.
        self.game = game

    def on_enter(self):
        """Se llama al entrar en esta pantalla."""

    def on_exit(self):
        """Se llama justo antes de salir de esta pantalla."""

    def handle_event(self, event):
        """Aqui gestionas teclado, raton y otros eventos."""

    def update(self, dt):
        """Aqui actualizas logica del juego."""

    def draw(self, surface):
        """Aqui dibujas la pantalla."""
