import math
import pygame

from game import config
from game.entities.entity import LivingEntity
from game.visuals.burn_flames import draw_burn_flames
from game.visuals.ice_block import ice_block_surfaces
from game.visuals.flying_shadow import flying_shadow
from game.visuals.poison_marks import draw_poison_mark
from game.visuals.fragile_mark import draw_fragile_crystal, draw_fragile_flecks


FLYING_SHADOW_GAP = 20


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

        self.puddle_slow_multiplier = 1.0
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
        self.burn_visual_time = 0
        self.burn_visual_phase = (x * 0.017 + y * 0.031) % 1
        self.freeze_fall_progress = 0
        self.poison_mark_stacks = 0
        self.poison_mark_pulse = 0
        self.fragile_visual_time = 0
        self.sentence_visual_active = False
        self.sentence_visual_pulse = 0

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
                "boss_stack_decay_interval": 0,
                "stack_decay_timer": 0,
                "is_stack_decay_active": False,
            },
            "fragile": {
                "timer": 0,
                "is_ready_to_execute": False,
                "is_sentenced": False,
                "sentence_threshold": 0,
                "execute_base_threshold": 0,
                "execute_threshold_per_stack": 0,
            },
        }

        self.visual = None

    def move(self, player, dt, blockers, entities, room=None):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance <= 0:
            return

        movement_speed = self.get_movement_speed()
        move_x = (diff_x / distance) * movement_speed * dt
        move_y = (diff_y / distance) * movement_speed * dt

        self.move_by(move_x, move_y, blockers, entities)

    def get_movement_speed(self):
        return self.speed

    @property
    def speed(self):
        return self._speed * self.puddle_slow_multiplier

    @speed.setter
    def speed(self, value):
        self._speed = value

    def update_status_effects(self, dt):
        self.update_burn(dt)
        self.update_ice(dt)
        self.update_poison(dt)
        poison_stacks = self.status_effects["poison"]["stacks"]
        if poison_stacks >= 5 and self.poison_mark_stacks < 5:
            self.poison_mark_pulse = 0.24
        else:
            self.poison_mark_pulse = max(0, self.poison_mark_pulse - dt)
        self.poison_mark_stacks = poison_stacks
        self.update_fragile(dt)
        self.fragile_visual_time += dt
        fragile = self.status_effects["fragile"]
        sentence_visible = (fragile["timer"] > 0 and fragile["is_sentenced"]
                            and self.health / self.max_health <= fragile["sentence_threshold"])
        if sentence_visible and not self.sentence_visual_active:
            self.sentence_visual_pulse = .28
        else:
            self.sentence_visual_pulse = max(0, self.sentence_visual_pulse - dt)
        self.sentence_visual_active = sentence_visible
        if getattr(self, "is_flying", False) and self.status_effects["ice"]["ice_timer"] > 0:
            self.freeze_fall_progress = min(1, self.freeze_fall_progress + dt / 0.16)
        elif getattr(self, "is_flying", False):
            self.freeze_fall_progress = max(0, self.freeze_fall_progress - dt / 0.7)
        else:
            self.freeze_fall_progress = 0

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
            self.burn_visual_time += dt
            burn["timer"] -= dt
            burn["tick_timer"] -= dt

            if burn["tick_timer"] <= 0:
                self.take_damage(burn["damage"])
                self.damage_flash_timer = 0.2
                burn["tick_timer"] = 1
        else:
            self.burn_visual_time = 0
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
                if (
                    getattr(self, "is_boss", False)
                    and poison["boss_stack_decay_interval"] > 0
                    and poison["stacks"] > 0
                ):
                    poison["is_stack_decay_active"] = True
                    poison["stack_decay_timer"] = (
                        poison["boss_stack_decay_interval"]
                    )
                else:
                    poison["stacks"] = 0
            return

        if not poison["is_stack_decay_active"]:
            return

        poison["stack_decay_timer"] -= dt
        if poison["stack_decay_timer"] > 0:
            return

        poison["stacks"] = max(0, poison["stacks"] - 1)
        if poison["stacks"] == 0:
            poison["stack_decay_timer"] = 0
            poison["is_stack_decay_active"] = False
        else:
            poison["stack_decay_timer"] = poison["boss_stack_decay_interval"]

    def update_fragile(self, dt):
        fragile = self.status_effects["fragile"]

        if fragile["timer"] > 0:
            fragile["timer"] -= dt

            if fragile["timer"] <= 0:
                fragile["timer"] = 0
                fragile["is_ready_to_execute"] = False
                fragile["is_sentenced"] = False
                fragile["sentence_threshold"] = 0

    def update(self, player, dt, blockers, entities, room=None):
        self.update_status_effects(dt)
        self.move(player, dt, blockers, entities, room)

        if self.visual is not None:
            self.visual.update(dt)

        self.update_visual_effects()
        self.update_knockback(dt, blockers, entities)
        return []
    
    def take_damage(self, damage):
        fragile = self.status_effects["fragile"]

        if (
            damage > 0
            and fragile["is_sentenced"]
            and self.health / self.max_health
            <= fragile["sentence_threshold"]
        ):
            self.health = 0
            self.damage_flash_timer = 0.15
            return

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


    def draw_ground_shadow(self, surface):
        if not getattr(self, "is_flying", False) or self.is_dead():
            return
        shadow = flying_shadow(max(12, round(self.radius * 1.8)))
        surface.blit(shadow, shadow.get_rect(center=(
            round(self.x), round(self.y + self.radius + FLYING_SHADOW_GAP)
        )))

    def draw(self, surface, visual_offset_y=0):

        sprite = self.visual.get_surface()

        if sprite is None:
            return

        # Pygame excludes both transparent pixels and the sprite's color key.
        visible_bounds = sprite.get_bounding_rect()
        frozen = (
            self.status_effects["ice"]["ice_timer"] > 0
            and not self.is_dead() and bool(visible_bounds)
        )
        fall_offset = visual_offset_y
        frozen_flyer = frozen and getattr(self, "is_flying", False)
        if getattr(self, "is_flying", False) and not self.is_dead():
            feet_offset = visible_bounds.bottom - sprite.get_height() // 2
            drop_distance = max(0, self.radius + FLYING_SHADOW_GAP - feet_offset)
            fall_offset = round(drop_distance * self.freeze_fall_progress ** 2)
        rect = sprite.get_rect(center=(int(self.x), int(self.y) + fall_offset))
        if frozen:
            ice_body_rect = visible_bounds.move(rect.topleft)
            ice_back, ice_front = ice_block_surfaces(
                ice_body_rect.width, ice_body_rect.height,
                self.status_effects["ice"].get("visual_variant", 0)
            )
            ice_rect = ice_back.get_rect(midbottom=(ice_body_rect.centerx, ice_body_rect.bottom + 6))
            if frozen_flyer:
                # Land the visible ice base and the sprite's feet on the shadow.
                ice_rect.bottom = ice_body_rect.bottom + 2
            surface.blit(ice_back, ice_rect)
        surface.blit(sprite, rect)

        self.draw_fragile_frost(surface, fall_offset)
        burn = self.status_effects["burn"]
        if burn["timer"] > 0 and not self.is_dead():
            draw_burn_flames(
                surface, rect, self.burn_visual_time,
                self.burn_visual_phase, burn["stacks"],
            )
        if frozen:
            surface.blit(ice_front, ice_rect)
        self.draw_status_marks(surface, fall_offset)
        self.draw_burn_stack_marks(surface, fall_offset)



    def draw_fragile_frost(self, surface, offset_y=0):
        fragile = self.status_effects["fragile"]
        health_ratio = self.health / self.max_health
        has_fragile_mark = (
            fragile["timer"] > 0
            and fragile["is_ready_to_execute"]
            and not fragile["is_sentenced"]
        )
        has_sentence_mark = (
            fragile["timer"] > 0
            and fragile["is_sentenced"]
            and health_ratio <= fragile["sentence_threshold"]
        )

        if not (has_fragile_mark or has_sentence_mark):
            return

        draw_fragile_flecks(surface, self.x, self.y + offset_y, self.radius,
                            self.fragile_visual_time + self.burn_visual_phase, has_sentence_mark)

    def draw_status_marks(self, surface, offset_y=0):
        marks = []
        
        poison = self.status_effects["poison"]

        poison_stacks = poison["stacks"]
        if poison_stacks >= 5:
            marks.append(("poison_full", (180, 80, 220)))
        else:
            for _ in range(poison_stacks):
                marks.append(("poison", (180, 80, 220)))
        
        fragile = self.status_effects["fragile"]
        health_ratio = self.health / self.max_health
        if (
            fragile["timer"] > 0
            and fragile["is_ready_to_execute"]
            and not fragile["is_sentenced"]
        ):
            marks.append(("fragile", (220, 240, 255)))

        if (
            fragile["is_sentenced"]
            and health_ratio <= fragile["sentence_threshold"]
        ):
            marks.append(("sentenced", (245, 190, 55)))

        if not marks:
            return

        mark_radius = 3
        widths = [22 if name == "poison_full" else 5 if name == "poison" else 26 if name == "sentenced" else 14
                  for name, _ in marks]
        spacing = 3
        total_width = sum(widths) + spacing * (len(marks) - 1)

        start_x = self.x - total_width / 2
        y = self.y - self.radius - 12 + offset_y

        for index, (_name, color) in enumerate(marks):
            x = start_x + widths[index] / 2
            start_x += widths[index] + spacing

            if _name == "fragile":
                self.draw_fragile_mark(surface, x, y, mark_radius)
            elif _name == "sentenced":
                self.draw_sentence_mark(surface, x, y, mark_radius)
            else:
                draw_poison_mark(surface, x, y, _name == "poison_full", self.poison_mark_pulse)

    def draw_fragile_mark(self, surface, x, y, radius):
        draw_fragile_crystal(surface, x, y)

    def draw_sentence_mark(self, surface, x, y, radius):
        draw_fragile_crystal(surface, x, y, sentenced=True, pulse=self.sentence_visual_pulse,
                             time=self.fragile_visual_time)

    def draw_burn_stack_marks(self, surface, offset_y=0):
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
        y = self.y - self.radius - 22 + offset_y

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
        
