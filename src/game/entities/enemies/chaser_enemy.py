"""Enemigo basico que solo persigue al jugador."""

import math
import random
import pygame

from game import config
from game.entities.enemies.enemy import Enemy


class ChaserEnemy(Enemy):
    def __init__(self, position):
        super().__init__(
            position=position,
            speed=config.ENEMY_SPEED,
            max_health=config.ENEMY_MAX_HEALTH,
            radius=config.ENEMY_RADIUS,
            color=config.ENEMY_COLOR,
            damage=config.ENEMY_DAMAGE,
            score_value=10,
        )


        self.detection_distance = 300

        self.random_dir_x = 0
        self.random_dir_y = 0
        self.random_move_timer = 0
        self.random_move_interval = 1.5

        self.setup_sprite(
            image_folder="enemies",
            image_name="rat.bmp",
            frame_cols=4,
            frame_rows=1,
            colorkey=(84, 206, 76),
            scale=5,
        )

        self.set_sprite_frame(2, 0)


    def choose_random_direction(self):
        self.random_dir_x = random.uniform(-1, 1)
        self.random_dir_y = random.uniform(-1, 1)

        length = math.hypot(self.random_dir_x, self.random_dir_y)

        if length > 0:
            self.random_dir_x /= length
            self.random_dir_y /= length


    def move(self, player, dt, blockers, entities):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance <= 0:
            return

        if distance <= self.detection_distance and not player.invulnerability_timer > 0:
            move_x = (diff_x / distance) * self.speed * dt
            move_y = (diff_y / distance) * self.speed * dt
        else:
            self.random_move_timer -= dt

            if self.random_move_timer <= 0:
                self.choose_random_direction()
                self.random_move_timer = self.random_move_interval

            move_x = self.random_dir_x * self.speed * dt
            move_y = self.random_dir_y * self.speed * dt

        if abs(move_x) > abs(move_y):
            if move_x > 0:
                self.set_sprite_frame(1, 0)  # derecha
            else:
                self.set_sprite_frame(0, 0)  # izquierda
        else:
            if move_y > 0:
                self.set_sprite_frame(2, 0)  # abajo
            else:
                self.set_sprite_frame(3, 0)  # arriba


        self.move_by(move_x, move_y, blockers, entities)


    def draw(self, surface):
        if self.sprite is None:
            super().draw(surface)
            return

        sprite_to_draw = self.sprite

        if self.damage_flash_timer > 0:
            mask = pygame.mask.from_surface(self.sprite)
            red_overlay = mask.to_surface(
                setcolor=(120, 0, 0, 180),
                unsetcolor=(0, 0, 0, 0),
            ).convert_alpha()

            sprite_to_draw = self.sprite.copy()
            sprite_to_draw.blit(red_overlay, (0, 0))

        sprite_rect = sprite_to_draw.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(sprite_to_draw, sprite_rect)