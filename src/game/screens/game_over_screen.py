"""Pantalla de game over, basada en la version simple."""

import pygame

from game import config
from game.screens.base_screen import BaseScreen
from game.ui.fonts import create_font


class GameOverScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.final_score = self.game.player.coins
        self.title_font = create_font(15)
        self.info_font = create_font(3)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.start_new_run()

            elif event.key == pygame.K_ESCAPE:
                from game.screens.menu_screen import MenuScreen

                self.game.screen_manager.set_screen(MenuScreen(self.game))

    def draw(self, surface):
        surface.fill(config.BACKGROUND_COLOR)

        surface_width = surface.get_width()
        surface_height = surface.get_height()

        title = self.title_font.render("Game Over", True, config.HUD_COLOR)
        score = self.info_font.render(f"Puntos: {self.final_score}", True, config.HUD_COLOR)
        info = self.info_font.render("Enter = jugar otra vez | Escape = menu", True, config.HUD_COLOR)

        surface.blit(title, title.get_rect(center=(surface_width // 2, surface_height // 2 - 10)))
        surface.blit(score, score.get_rect(center=(surface_width // 2, surface_height // 2 + 10)))
        surface.blit(info, info.get_rect(center=(surface_width // 2, surface_height // 2 + 20)))