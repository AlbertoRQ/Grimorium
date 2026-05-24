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
        
        self.base_speed = self.speed
        self.base_color = color

        self.damage_flash_timer = 0

        self.status_effects = {
            "burn": {
                "is_burned": False,
                "timer": 0,
                "tick_timer": 0,
                "damage": 0,
            },
            "ice": {
                "is_slowed": False,
                "slow_timer": 0,
                "multiplier": 0,
                "stacks": 0,
                "is_ice": False,
                "ice_timer": 0,
                "ice_cooldown": 0,
                "cooldown_value": 0,

            },
            "shock": {
                "timer": 0,
            },
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
        self.update_burn(dt)
        self.update_ice(dt)
        #self.update_shock(dt)
        #self.update_visual_effects(dt)

    
    def update_burn(self, dt):
        burn = self.status_effects["burn"]
        
        if burn["timer"] > 0:
            burn["timer"] -= dt
            burn["tick_timer"] -= dt

            if burn["tick_timer"] <= 0:
                self.take_damage(burn["damage"])
                self.damage_flash_timer = 0.2
                burn["tick_timer"] = 1
        else:
            burn["is_burned"] = False

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= dt
            r, g, b = self.base_color
            self.color = (int(r * 0.5), int(g * 0.5), int(b * 0.5))
        else:
            self.color = self.base_color


    def update_ice(self, dt):
        ice = self.status_effects["ice"]

        if ice["ice_cooldown"] > 0:
            ice["ice_cooldown"] -= dt
            if ice["ice_cooldown"] < 0:
                ice["ice_cooldown"] = 0

        if ice["ice_timer"] > 0:
            ice["ice_timer"] -= dt
            self.speed = 0

            r, g, b = self.base_color
            self.color = (
                min(255, int(r * 0.3 + 100)),
                min(255, int(g * 0.3 + 140)),
                min(255, int(b * 0.8 + 180)),
            )

            if ice["ice_timer"] <= 0:
                ice["is_ice"] = False
                ice["is_slowed"] = False
                ice["slow_timer"] = 0
                ice["stacks"] = 0
                ice["ice_timer"] = 0
                ice["ice_cooldown"] = ice["cooldown_value"]
                self.speed = self.base_speed
                self.color = self.base_color

            return

        if ice["slow_timer"] > 0:
            ice["slow_timer"] -= dt
            self.speed = self.base_speed * ice["multiplier"]

            r, g, b = self.base_color
            self.color = (
                int(r * 0.6),
                int(g * 0.8),
                min(255, int(b * 1.2)),
            )
        else:
            ice["is_slowed"] = False
            ice["stacks"] = 0
            self.speed = self.base_speed

    def update(self, player, dt, blockers, entities):
        self.update_status_effects(dt)
        self.move(player, dt, blockers, entities)
        return []
