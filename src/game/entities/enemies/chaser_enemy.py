"""Enemigo basico que solo persigue al jugador."""

import math
import random
import pygame

from game import config
from game.entities.enemies.enemy import Enemy
from game.visuals.animated_visual import AnimatedVisual


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

        self.visual = AnimatedVisual(
            image_folder="enemies/rat",
            image_name="rat_animated.png",
            frame_cols=4,
            frame_rows=4,
            scale_x=self.radius * 5,
            scale_y=self.radius * 5,
            use_alpha=True,
            initial_state="idle",
            initial_facing="down",
            animations={
                "idle_right": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                "walk_right": {"row": 0, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_left": {"row": 1, "frames": [0], "speed": 0.25, "loop": True},
                "walk_left": {"row": 1, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_down": {"row": 2, "frames": [0], "speed": 0.25, "loop": True},
                "walk_down": {"row": 2, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_up": {"row": 3, "frames": [0], "speed": 0.25, "loop": True},
                "walk_up": {"row": 3, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},
            },
        )

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

        old_x = self.x
        old_y = self.y

        self.move_by(move_x, move_y, blockers, entities)

        real_move_x = self.x - old_x
        real_move_y = self.y - old_y

        self.update_visual_from_movement(real_move_x, real_move_y)