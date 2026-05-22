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

        super().__init__(x, y, radius, color, color, max_health)

        self.speed = speed
        self.damage = damage
        self.body_damage = config.ENEMY_BODY_DAMAGE
        self.score_value = score_value

        self.is_burned = False
        self.damage_flash_timer = 0

        self.status_effects = {
            "burn": {"timer": 0, "tick_timer": 0},
            "slow": {"timer": 0, "multiplier": 1.0},
            "shock": {"timer": 0},
        }

    def move(self, player, dt, blockers, entities):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance <= 0:
            return

        move_x = (diff_x / distance) * self.speed * dt
        move_y = (diff_y / distance) * self.speed * dt

        self.move_by(move_x, move_y, blockers, entities)

    def update_status_effects(self, dt):
        burn = self.status_effects["burn"]
        
        if burn["timer"] > 0:
            burn["timer"] -= dt
            burn["tick_timer"] -= dt

            if burn["tick_timer"] <= 0:
                self.take_damage(burn["damage"])
                self.damage_flash_timer = 0.2
                burn["tick_timer"] = 1
        else:
            self.is_burned = False

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= dt
            r, g, b = self.base_color
            self.color = (int(r * 0.5), int(g * 0.5), int(b * 0.5))
        else:
            self.color = self.base_color


    def update(self, player, dt, blockers, entities):
        self.update_status_effects(dt)
        self.move(player, dt, blockers, entities)
        return []
