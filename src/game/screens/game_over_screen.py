"""Pantalla de game over, basada en la version simple."""

import pygame

from game import config
from game.screens.base_screen import BaseScreen


class GameOverScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.final_score = self.game.player.coins
        self.title_font = pygame.font.Font(None, 72)
        self.info_font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from game.screens.play_screen import PlayScreen
                self.game.start_new_run()
                self.game.screen_manager.set_screen(PlayScreen(self.game))
            elif event.key == pygame.K_ESCAPE:
                from game.screens.menu_screen import MenuScreen

                self.game.screen_manager.set_screen(MenuScreen(self.game))

    def draw(self, surface):
        surface.fill(config.BACKGROUND_COLOR)

        title = self.title_font.render("Game Over", True, config.HUD_COLOR)
        score = self.info_font.render(f"Puntos: {self.final_score}", True, config.HUD_COLOR)
        info = self.info_font.render("Enter = jugar otra vez | Escape = menu", True, config.HUD_COLOR)

        surface.blit(title, title.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 60)))
        surface.blit(score, score.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)))
        surface.blit(info, info.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 50)))
