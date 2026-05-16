"""Pantalla de menu, basada en la version simple."""

import pygame

from game import config
from game.screens.base_screen import BaseScreen


class MenuScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 72)
        self.info_font = pygame.font.Font(None, 36)


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.start_new_run()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.start_boss_test()


    def draw(self, surface):
        surface.fill(config.BACKGROUND_COLOR)

        title = self.title_font.render("Mi juego", True, config.HUD_COLOR)
        normal_play = self.info_font.render("Pulsa Enter para jugar", True, config.HUD_COLOR)
        boss_test = self.info_font.render("Pulsa Espacio para test del jefe", True, config.HUD_COLOR)

        surface.blit(title, title.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 40)))
        surface.blit(normal_play, normal_play.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 20)))
        surface.blit(boss_test, boss_test.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 40)))
