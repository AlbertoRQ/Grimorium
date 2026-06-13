"""Pantalla de menu, basada en la version simple."""

import pygame

from game import config
from game.screens.base_screen import BaseScreen
from game.ui.fonts import create_font


class MenuScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = create_font(15)
        self.info_font = create_font(3)


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.start_new_run()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.start_boss_test()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
            self.game.toggle_fullscreen()

    def draw(self, surface):
        surface.fill(config.BACKGROUND_COLOR)

        surface_width = surface.get_width()
        surface_height = surface.get_height()

        title = self.title_font.render("GRIMORIUM", True, config.HUD_COLOR)
        normal_play = self.info_font.render("Pulsa Enter para jugar", True, config.HUD_COLOR)
        boss_test = self.info_font.render("Pulsa Espacio para test del jefe", True, config.HUD_COLOR)
        fullscreen = self.info_font.render("Pulsa F12 para pantalla completa", True, config.HUD_COLOR)


        surface.blit(title, title.get_rect(center=(surface_width // 2, surface_height // 2 - 10)))
        surface.blit(normal_play, normal_play.get_rect(center=(surface_width // 2, surface_height // 2 + 10)))
        surface.blit(boss_test, boss_test.get_rect(center=(surface_width // 2, surface_height // 2 + 20)))
        surface.blit(fullscreen, fullscreen.get_rect(center=(surface_width // 2, surface_height // 2 + 30)))