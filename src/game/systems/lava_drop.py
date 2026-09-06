import math

import pygame

from game.systems.effect_handlers import apply_fire_data


class LavaDrop:
    def __init__(
        self,
        x,
        start_y,
        target_y,
        radius,
        fall_duration,
        fire_data,
    ):
        self.x = x
        self.start_y = start_y
        self.target_y = target_y
        self.radius = radius
        self.fall_duration = fall_duration
        self.fire_data = fire_data

        self.timer = 0
        self.y = start_y
        self.finished = False

    def update(self, dt, enemies):
        self.timer += dt
        progress = min(1, self.timer / self.fall_duration)
        self.y = self.start_y + (self.target_y - self.start_y) * progress

        if progress < 1:
            return

        for enemy in enemies:
            if enemy.is_dead():
                continue

            distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if distance <= self.radius + enemy.radius:
                apply_fire_data(enemy, self.fire_data)

        self.finished = True

    def draw(self, surface):
        if self.finished:
            return

        pygame.draw.circle(
            surface,
            (255, 100, 35),
            (int(self.x), int(self.y)),
            self.radius + 1,
        )
        pygame.draw.circle(
            surface,
            (255, 220, 95),
            (int(self.x), int(self.y)),
            self.radius,
        )
