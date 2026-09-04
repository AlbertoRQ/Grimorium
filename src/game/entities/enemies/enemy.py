import math
import pygame

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
                "stacks": 0,
                "hits_to_next_stack": 0,
                "max_stacks": 1,
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
            "poison": {
                "stacks": 0,
                "timer": 0,
                "max_stacks": 5,
                "damage_taken_per_stack": 0.05,
            },
            "fragile": {
                "timer": 0,
            },
        }

        self.visual = None

    def move(self, player, dt, blockers, entities, room=None):
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
        self.update_poison(dt)
        self.update_fragile(dt)

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
            burn["tick_timer"] = 0
            burn["damage"] = 0
            burn["stacks"] = 0
            burn["hits_to_next_stack"] = 0
            burn["max_stacks"] = 1

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

    def update_poison(self, dt):
        poison = self.status_effects["poison"]

        if poison["timer"] > 0:
            poison["timer"] -= dt
            if poison["timer"] <= 0:
                poison["timer"] = 0
                poison["stacks"] = 0

    def update_fragile(self, dt):
        fragile = self.status_effects["fragile"]

        if fragile["timer"] > 0:
            fragile["timer"] -= dt

            if fragile["timer"] < 0:
                fragile["timer"] = 0

    def update(self, player, dt, blockers, entities, room=None):
        self.update_status_effects(dt)
        self.move(player, dt, blockers, entities, room)

        if self.visual is not None:
            self.visual.update(dt)

        self.update_visual_effects()
        self.update_knockback(dt, blockers, entities)
        return []
    
    def take_damage(self, damage):

        poison = self.status_effects.get("poison")

        if poison is not None and poison["stacks"] > 0:
            bonus = poison["stacks"] * poison["damage_taken_per_stack"]
            damage *= 1 + bonus

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

        self.draw_status_marks(surface)
        self.draw_burn_stack_marks(surface)



    def draw_status_marks(self, surface):
        marks = []
        
        poison = self.status_effects["poison"]

        poison_stacks = poison["stacks"]
        for _ in range(poison_stacks):
            marks.append(("poison", (180, 80, 220)))
        
        fragile = self.status_effects["fragile"]

        if fragile["timer"] > 0:
            marks.append(("fragile", (220, 240, 255)))

        if not marks:
            return

        mark_radius = 3
        spacing = 8
        total_width = (len(marks) - 1) * spacing

        start_x = self.x - total_width / 2
        y = self.y - self.radius - 12

        for index, (_name, color) in enumerate(marks):
            x = start_x + index * spacing

            pygame.draw.circle(
                surface,
                (20, 20, 25),
                (int(x), int(y)),
                mark_radius + 1,
            )

            pygame.draw.circle(
                surface,
                color,
                (int(x), int(y)),
                mark_radius,
            )

    def draw_burn_stack_marks(self, surface):
        burn = self.status_effects["burn"]

        if not burn["is_burned"] or burn["max_stacks"] <= 1:
            return

        marks = []

        extra_stacks = burn["stacks"] - 1
        for _ in range(extra_stacks):
            marks.append(("stack", 5, (255, 80, 25)))

        for _ in range(burn["hits_to_next_stack"]):
            marks.append(("progress", 3, (255, 155, 35)))

        if not marks:
            return

        spacing = 11
        total_width = (len(marks) - 1) * spacing
        start_x = self.x - total_width / 2
        y = self.y - self.radius - 22

        for index, (_name, radius, color) in enumerate(marks):
            x = start_x + index * spacing

            pygame.draw.circle(
                surface,
                (35, 15, 10),
                (int(x), int(y)),
                radius + 1,
            )

            pygame.draw.circle(
                surface,
                color,
                (int(x), int(y)),
                radius,
            )
        