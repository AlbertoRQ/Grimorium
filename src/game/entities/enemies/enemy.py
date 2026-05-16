"""Enemigo base."""

import math

from game import config
from game.entities.entity import LivingEntity


class Enemy(LivingEntity):
    def __init__(
        self,
        position,
        speed,
        max_health,
        radius,
        color,
        damage,
        score_value,
    ):
        x, y = position

        super().__init__(x, y, radius, color, max_health)

        self.speed = speed
        self.damage = damage
        self.body_damage = config.ENEMY_BODY_DAMAGE
        self.score_value = score_value

    def move(self, player, dt, blockers, entities):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance <= 0:
            return

        move_x = (diff_x / distance) * self.speed * dt
        move_y = (diff_y / distance) * self.speed * dt

        self.move_by(move_x, move_y, blockers, entities)

    def update(self, player, dt, blockers, entities):
        self.move(player, dt, blockers, entities)
        return []
