"""Bucle principal del juego.

Este archivo es el "corazon" del proyecto.
Lo normal es que aqui no metas logica de enemigos o balas:
solo coordina el juego y deja el trabajo a las pantallas.
"""

import pygame

from game import config
from game.core.screen_manager import ScreenManager
from game.entities.player import Player
from game.config import RUN_PATTERN

from game.screens.menu_screen import MenuScreen
from game.screens.play_screen import PlayScreen
from game.screens.shop_screen import ShopScreen
from game.screens.boss_screen import BossScreen
from game.screens.game_over_screen import GameOverScreen



class Game:
    """Objeto principal que arranca pygame y mantiene el bucle general."""

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_manager = ScreenManager()

        self.run_step = 0
        self.current_step = self.run_step
        self.run_cycles = 0
        self.max_cycles = 3
        self.player = Player()

        self.room_level = 1

        # La primera pantalla sera el menu.
        self.screen_manager.set_screen(MenuScreen(self))

    def go_to_next_run_screen(self):
        step = RUN_PATTERN[self.run_step]

        self.run_step += 1
        if self.run_step >= len(RUN_PATTERN):
            self.run_step = 0

        self.current_step = step

        if step == "normal":
            self.screen_manager.set_screen(PlayScreen(self))
        elif step == "shop":
            self.screen_manager.set_screen(ShopScreen(self))
        elif step == "boss":
            self.screen_manager.set_screen(BossScreen(self))
        else:
            raise ValueError(f"Paso desconocido: {step}")


    def finish_current_screen(self):
        if self.mode == "boss_test":
                self.screen_manager.set_screen(MenuScreen(self))
                return
        
        if self.current_step == "normal":
            self.room_level += 1

        if self.current_step == "boss":
            self.run_cycles += 1

            if self.run_cycles >= self.max_cycles:
                self.screen_manager.set_screen(GameOverScreen(self))
                return

        self.go_to_next_run_screen()

    def start_new_run(self):
        self.mode = "normal_run"
        self.run_step = 0
        self.current_step = None
        self.run_cycles = 0
        self.room_level = 1
        self.player = Player()

        self.go_to_next_run_screen()

    def start_boss_test(self):
        self.player = Player()
        self.mode = "boss_test"

        self.screen_manager.set_screen(BossScreen(self))

    def run(self):
        """Bucle principal.

        Pasos de cada vuelta:
        1. leer eventos
        2. actualizar la pantalla actual
        3. dibujar la pantalla actual
        """
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                self.screen_manager.handle_event(event)

            self.screen_manager.update(dt)

            self.screen.fill(config.BACKGROUND_COLOR)
            self.screen_manager.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
