"""Pantalla de pausa."""

import pygame

from game import config
from game.screens.base_screen import BaseScreen
from game.ui.button import Button


class PauseScreen(BaseScreen):
    def __init__(self, game, previous_screen):
        super().__init__(game)
        self.previous_screen = previous_screen
        center_x = config.SCREEN_WIDTH // 2

        self.title_font = pygame.font.Font(None, 82)
        self.buttons = [
            Button((center_x - 120, 300, 240, 60), "Continuar", self._resume),
            Button((center_x - 120, 380, 240, 60), "Menu", self._go_menu),
        ]

    def _resume(self):
        self.game.screen_manager.set_screen(self.previous_screen)

    def _go_menu(self):
        from game.screens.menu_screen import MenuScreen

        self.game.screen_manager.set_screen(MenuScreen(self.game))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._resume()
            return

        for button in self.buttons:
            button.handle_event(event)

    def draw(self, surface):
        # Dibujamos antes la partida congelada debajo.
        self.previous_screen.draw(surface)

        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        title = self.title_font.render("Pausa", True, config.HUD_COLOR)
        surface.blit(title, title.get_rect(center=(config.SCREEN_WIDTH / 2, 180)))

        for button in self.buttons:
            button.draw(surface)
