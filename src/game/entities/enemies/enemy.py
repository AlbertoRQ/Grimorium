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

        self.knockback_x = 0
        self.knockback_y = 0
        self.knockback_friction = 8

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

        self.visual = None

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

    def update_visual_effects(self):
        ice = self.status_effects["ice"]
        burn = self.status_effects["burn"]

        if self.visual is None:
            if ice["ice_timer"] > 0:
                r, g, b = self.base_color
                self.color = (
                    min(255, int(r * 0.3 + 100)),
                    min(255, int(g * 0.3 + 140)),
                    min(255, int(b * 0.8 + 180)),
                )
            elif self.damage_flash_timer > 0:
                r, g, b = self.base_color
                self.color = (int(r * 0.5), int(g * 0.5), int(b * 0.5))
            elif ice["slow_timer"] > 0:
                r, g, b = self.base_color
                self.color = (
                    int(r * 0.6),
                    int(g * 0.8),
                    min(255, int(b * 1.2)),
                )
            elif burn["timer"] > 0:
                r, g, b = self.base_color
                self.color = (
                    int(r * 0.5),
                    int(g * 0.5),
                    int(b * 0.5),
                )
            else:
                self.color = self.base_color

            return

        if ice["ice_timer"] > 0:
            self.visual.set_tint((200, 230, 255, 180))
        elif self.damage_flash_timer > 0:
            self.visual.set_tint((120, 0, 0, 180))
        elif ice["slow_timer"] > 0:
            self.visual.set_tint((80, 140, 220, 140))
        elif burn["timer"] > 0:
            self.visual.set_tint((80, 30, 30, 140))
        else:
            self.visual.clear_tint()

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
            burn["timer"] = 0

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= dt
            if self.damage_flash_timer < 0:
                self.damage_flash_timer = 0

    def update_ice(self, dt):
        ice = self.status_effects["ice"]

        if ice["ice_cooldown"] > 0:
            ice["ice_cooldown"] -= dt
            if ice["ice_cooldown"] < 0:
                ice["ice_cooldown"] = 0

        if ice["ice_timer"] > 0:
            ice["ice_timer"] -= dt
            self.speed = 0

            if ice["ice_timer"] <= 0:
                ice["is_ice"] = False
                ice["is_slowed"] = False
                ice["slow_timer"] = 0
                ice["stacks"] = 0
                ice["ice_timer"] = 0
                ice["ice_cooldown"] = ice["cooldown_value"]
                self.speed = self.base_speed

            return

        if ice["slow_timer"] > 0:
            ice["slow_timer"] -= dt
            self.speed = self.base_speed * ice["multiplier"]

            if ice["slow_timer"] <= 0:
                ice["slow_timer"] = 0
                ice["is_slowed"] = False
                ice["stacks"] = 0
                self.speed = self.base_speed
        else:
            ice["is_slowed"] = False
            ice["stacks"] = 0
            self.speed = self.base_speed

    def update(self, player, dt, blockers, entities):
        self.update_status_effects(dt)
        self.move(player, dt, blockers, entities)

        if self.visual is not None:
            self.visual.update(dt)

        self.update_visual_effects()
        self.update_knockback(dt, blockers, entities)
        return []
    
    def take_damage(self, damage):
        if damage > 0:
            self.health = max(0, self.health - damage)
            self.damage_flash_timer = 0.15

    def apply_knockback(self, dir_x, dir_y, strength):
        self.knockback_x += dir_x * strength
        self.knockback_y += dir_y * strength

    def update_knockback(self, dt, blockers, entities):
        if abs(self.knockback_x) < 1 and abs(self.knockback_y) < 1:
            self.knockback_x = 0
            self.knockback_y = 0
            return

        move_x = self.knockback_x * dt
        move_y = self.knockback_y * dt

        self.move_by(move_x, move_y, blockers, entities)

        decay = max(0, 1 - self.knockback_friction * dt)
        self.knockback_x *= decay
        self.knockback_y *= decay


    def update_visual_from_movement(self, move_x, move_y):
        if abs(move_x) > abs(move_y):
            if move_x > 0:
                self.visual.set_facing("right")
            elif move_x < 0:
                self.visual.set_facing("left")
        else:
            if move_y > 0:
                self.visual.set_facing("down")
            elif move_y < 0:
                self.visual.set_facing("up")

        if move_x != 0 or move_y != 0:
            self.visual.set_state("walk")
        else:
            self.visual.set_state("idle")


    def draw(self, surface):
        sprite = self.visual.get_surface()

        if sprite is None:
            return

        rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(sprite, rect)