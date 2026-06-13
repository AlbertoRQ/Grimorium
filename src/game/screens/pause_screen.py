"""Pantalla de pausa."""

import pygame

from game import config
from game.screens.base_screen import BaseScreen
from game.ui.button import Button
from game.ui.fonts import create_font


class PauseScreen(BaseScreen):
    def __init__(self, game, previous_screen):
        super().__init__(game)
        self.previous_screen = previous_screen
        center_x = self.VIRTUAL_WIDTH // 2

        self.title_font = create_font(15)
        self.buttons = [
            Button((center_x - 120, 300, 240, 60), "Continuar", self._resume),
            Button((center_x - 120, 380, 240, 60), "Menu", self._go_menu),
        ]

        self.overlay = pygame.Surface((self.VIRTUAL_WIDTH, self.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))

    def _resume(self):
        self.game.screen_manager.set_screen(self.previous_screen)

    def _go_menu(self):
        from game.screens.menu_screen import MenuScreen

        self.game.screen_manager.set_screen(MenuScreen(self.game))

    def screen_to_virtual(self, pos):
        mx, my = pos
        return (
            (mx - self.game.render_offset_x) // self.game.render_scale,
            (my - self.game.render_offset_y) // self.game.render_scale,
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._resume()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = self.screen_to_virtual(event.pos)

            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.callback()

    def draw(self, surface):
        # Dibujamos antes la partida congelada debajo.
        self.previous_screen.draw(surface)

        surface_width = surface.get_width()

        surface.blit(self.overlay, (0, 0))

        title = self.title_font.render("Pausa", True, config.HUD_COLOR)
        surface.blit(title, title.get_rect(center=(surface_width // 2, 80)))

        mouse_pos = self.screen_to_virtual(pygame.mouse.get_pos())

        for button in self.buttons:
            button.draw(surface, mouse_pos)