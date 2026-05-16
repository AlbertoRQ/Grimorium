"""Disparo en abanico."""

import pygame

from game import config
from game.entities.bullets.bullet import Bullet


class SpreadBullet(Bullet):
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__(x, y, vel_x, vel_y)
        self.color = (200, 0, 255)
        self.radius = 15
        self.rate = 2


def create_spread_shot(x, y, vel_x, vel_y):
    bullets = []
    base_velocity = pygame.Vector2(vel_x, vel_y)
    total = config.SPREAD_BULLET_COUNT
    middle_index = (total - 1) / 2

    for index in range(total):
        angle = (index - middle_index) * config.SPREAD_ANGLE_STEP
        rotated_velocity = base_velocity.rotate(angle)
        bullets.append(SpreadBullet(x, y, rotated_velocity.x, rotated_velocity.y))

    return bullets, bullets[0].rate
