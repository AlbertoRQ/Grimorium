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

        self.screen = None
        self.is_fullscreen = False
        self.apply_display_mode()
        pygame.display.set_caption(config.WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_manager = ScreenManager()

        self.run_step = 0
        self.current_step = self.run_step
        self.current_step_index = 0
        self.run_cycles = 0
        self.max_cycles = 3
        self.player = Player()

        self.room_level = 1

        # La primera pantalla sera el menu.
        self.screen_manager.set_screen(MenuScreen(self))

        self.debug_font = pygame.font.Font(None, 24)
        self.show_fps = True       


    def go_to_next_run_screen(self):
        self.current_step_index = self.run_step
        step = RUN_PATTERN[self.current_step_index]

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

        if self.is_last_step_of_loop():
            self.run_cycles += 1

            if self.run_cycles >= self.max_cycles:
                self.screen_manager.set_screen(GameOverScreen(self))
                return

            self.room_level = 1

        self.go_to_next_run_screen()

    def is_last_step_of_loop(self):
        for index in range(len(RUN_PATTERN) - 1, -1, -1):
            if RUN_PATTERN[index] != "shop":
                return self.current_step_index == index

        return False

    def start_new_run(self):
        self.mode = "normal_run"
        self.run_step = 0
        self.current_step = None
        self.current_step_index = 0
        self.run_cycles = 0
        self.room_level = 1
        self.player = Player()

        self.go_to_next_run_screen()

    def start_boss_test(self):
        self.player = Player()
        self.mode = "boss_test"

        self.screen_manager.set_screen(BossScreen(self))


    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                self.screen_manager.handle_event(event)

            self.screen_manager.update(dt)

            current_screen = self.screen_manager.current_screen
            self.update_render_metrics(current_screen)
            virtual_surface = current_screen.virtual_surface

            virtual_surface.fill(config.BACKGROUND_COLOR)
            current_screen.draw(virtual_surface)

            scaled_surface = pygame.transform.scale(
                virtual_surface,
                (self.render_width, self.render_height)
            )

            self.screen.fill((0, 0, 0))
            self.screen.blit(
                scaled_surface,
                (self.render_offset_x, self.render_offset_y)
            )

            if self.show_fps:
                fps = self.clock.get_fps()
                ms = 1000 / fps if fps > 0 else 0
                fps_text = self.debug_font.render(f"FPS: {fps:.1f}  MS: {ms:.2f}", True, (255, 255, 0))
                self.screen.blit(fps_text, (20, 20))

            pygame.display.flip()

        pygame.quit()


    def update_render_metrics(self, current_screen):
        vw, vh = current_screen.get_virtual_size()

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.render_scale = min(
            screen_width // vw,
            screen_height // vh,
        )

        self.render_width = vw * self.render_scale
        self.render_height = vh * self.render_scale

        self.render_offset_x = (screen_width - self.render_width) // 2
        self.render_offset_y = (screen_height - self.render_height) // 2

    def apply_display_mode(self):
        if self.is_fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode(
                (info.current_w, info.current_h),
                pygame.FULLSCREEN | pygame.SCALED
            )
        else:
            self.screen = pygame.display.set_mode(
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
                pygame.SCALED
            )

        pygame.display.set_caption(config.WINDOW_TITLE)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.apply_display_mode()