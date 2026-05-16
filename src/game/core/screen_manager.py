"""Gestiona que pantalla esta activa en cada momento."""


class ScreenManager:
    """Guarda la pantalla actual y la cambia cuando haga falta."""

    def __init__(self):
        self.current_screen = None

    def set_screen(self, new_screen):
        """Cambia de pantalla.

        Si la pantalla anterior necesita limpiar algo, usa `on_exit`.
        Si la nueva necesita prepararse, usa `on_enter`.
        """
        if self.current_screen is not None:
            self.current_screen.on_exit()

        self.current_screen = new_screen

        if self.current_screen is not None:
            self.current_screen.on_enter()

    def handle_event(self, event):
        if self.current_screen is not None:
            self.current_screen.handle_event(event)

    def update(self, dt):
        if self.current_screen is not None:
            self.current_screen.update(dt)

    def draw(self, surface):
        if self.current_screen is not None:
            self.current_screen.draw(surface)
