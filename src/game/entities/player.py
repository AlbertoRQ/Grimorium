"""Jugador sencillo, basado en la version que ya tenias clara."""

import math
import pygame
import random

from game import config
from game.entities.bullets.bullet import create_gatling_shot
from game.entities.bullets.bullet import create_normal_shot
from game.entities.bullets.bullet import create_spread_shot
from game.entities.entity import LivingEntity
from game.entities.items.item_data import ITEM_DEFINITIONS 
from game.visuals.animated_visual import AnimatedVisual

SHOT_FACTORIES = {
    "normal": create_normal_shot,
    "gatling": create_gatling_shot,
    "spread": create_spread_shot,
}

class Player(LivingEntity):
    def __init__(self):
        super().__init__(
            config.SCREEN_WIDTH / 2,
            config.SCREEN_HEIGHT / 2,
            config.PLAYER_RADIUS,
            config.PLAYER_COLOR,
            config.PLAYER_COLOR,
            config.PLAYER_MAX_HEALTH,
        )

        self.body_damage = config.PLAYER_BODY_DAMAGE
        self.damage = config.PLAYER_DAMAGE
        self.fire_rate = config.PLAYER_FIRE_COOLDOWN
        self.speed = config.PLAYER_SPEED
        self.luck = config.PLAYER_LUCK
        self.shoot_distance = config.PLAYER_SHOOT_DISTANCE
        

        self.shoot_timer = 0
        self.bullet_type = "normal"
        self.base_bullet_elements = []
        self.extra_bullet_element = {}
        self.element_stats = {
            "fire": {
                "level": 9,
                "burn_duration": 3,
                "burn_damage": 0.5,
                "burn_tick_timer": 0.5,
            },
            "ice": {
                "level": 1,
                "slow_duration": 2,
                "slow_multiplier": 0.9,
                "max_ice_stacks": 5,
                "ice_duration": 1.5,
                "ice_cooldown": 2,
            },
            "electric": {},
        }
        
        self.combo_stats = {
            "fire_ice": {
                "level": 1,
                "damage_multiplier": 2.0,
            },
        }

        self.invulnerability_timer = 0

        self.coins = 0
        self.items = []

        self.move_dir_x = 0
        self.move_dir_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 2000
        self.friction = 2000
        self.max_speed = config.PLAYER_SPEED

        self.visual = AnimatedVisual(
            image_folder="player",
            image_name="mage_animated.png",
            frame_cols=4,
            frame_rows=4,
            scale_x=self.radius * 3,
            scale_y=self.radius * 3,
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

    def move(self, keys, dt, blockers, entities):
        move_x = 0
        move_y = 0

        if keys[pygame.K_d]:
            move_x += 1
        if keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_s]:
            move_y += 1

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

        length = math.hypot(move_x, move_y)

        if length > 0:
            self.visual.set_state("walk")
            move_x /= length
            move_y /= length
        else:
            self.visual.set_state("idle")

        self.velocity_x += move_x * self.acceleration * dt
        self.velocity_y += move_y * self.acceleration * dt

        speed = math.hypot(self.velocity_x, self.velocity_y)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity_x *= scale
            self.velocity_y *= scale

        if move_x == 0:
            if self.velocity_x > 0:
                self.velocity_x = max(0, self.velocity_x - self.friction * dt)
            elif self.velocity_x < 0:
                self.velocity_x = min(0, self.velocity_x + self.friction * dt)

        if move_y == 0:
            if self.velocity_y > 0:
                self.velocity_y = max(0, self.velocity_y - self.friction * dt)
            elif self.velocity_y < 0:
                self.velocity_y = min(0, self.velocity_y + self.friction * dt)

        self.move_by(self.velocity_x * dt, self.velocity_y * dt, blockers, entities)
        

    def update(self, dt):
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if self.invulnerability_timer > 0:
            self.color = config.PLAYER_COLOR_INVENCIBLE
            self.invulnerability_timer -= dt
        
        if self.invulnerability_timer <= 0:
            self.color = config.PLAYER_COLOR

        self.visual.update(dt)

    def take_damage(self, damage):
        if self.invulnerability_timer > 0:
            return

        self.health = max(0, self.health - damage)
        self.invulnerability_timer = config.PLAYER_INVULNERABILITY_TIME

    def shoot(self, keys):

        if self.shoot_timer > 0:
            return []

        shoot_x = 0
        shoot_y = 0

        if keys[pygame.K_RIGHT]:
            shoot_x += 1
        if keys[pygame.K_LEFT]:
            shoot_x -= 1
        if keys[pygame.K_UP]:
            shoot_y -= 1
        if keys[pygame.K_DOWN]:
            shoot_y += 1

        length = math.hypot(shoot_x, shoot_y)
        if length > 0:
            shoot_x /= length
            shoot_y /= length

        move_speed = math.hypot(self.velocity_x, self.velocity_y)

        if move_speed > 0:
            move_dir_x = self.velocity_x / move_speed
            move_dir_y = self.velocity_y / move_speed
        else:
            move_dir_x = 0
            move_dir_y = 0

        speed_factor = move_speed / self.max_speed
        speed_factor = min(speed_factor, 1)

        forward_amount = (move_dir_x * shoot_x + move_dir_y * shoot_y) * speed_factor
        right_x = -shoot_y
        right_y = shoot_x
        side_amount = (move_dir_x * right_x + move_dir_y * right_y) * speed_factor

        distance = math.hypot(shoot_x, shoot_y)

        if distance <= 0:
            return []

        bullet_speed = config.BULLET_SPEED + forward_amount * config.FORWARD_BONUS

        vel_x = shoot_x * bullet_speed + right_x * side_amount * config.SIDE_DRIFT
        vel_y = shoot_y * bullet_speed + right_y * side_amount * config.SIDE_DRIFT


        elements = self.base_bullet_elements.copy()

        for element, chance in self.extra_bullet_element.items():
            if random.random() < chance:
                elements.append(element)

        effect_data = {}
        effect_data["combos"] = {
            "fire_ice": self.combo_stats["fire_ice"].copy(),
        }
        for element in elements:
            if element in self.element_stats:
                effect_data[element] = self.element_stats[element].copy()
        factory = SHOT_FACTORIES[self.bullet_type]
        shoot, rate = factory(self.x, self.y, vel_x, vel_y, self.shoot_distance, elements, effect_data)
        
        self.shoot_timer = self.fire_rate * rate
        return shoot


    def draw_player_health(self, surface, font):
        bar_width = 200 
        bar_height = 60

        x = 185
        y = 15

        health_ratio = self.health / self.max_health
        health_ratio = max(0, min(1, health_ratio))

        fill_width = int(bar_width * health_ratio)

        background_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill_width, bar_height)

        pygame.draw.rect(surface, (50, 50, 50), background_rect)
        pygame.draw.rect(surface, (200, 30, 30), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), background_rect, 2)

        text = font.render(
            f"{int(self.health)} / {self.max_health}",
            True,
            (255, 255, 255),
        )

        text_rect = text.get_rect(center=background_rect.center)
        surface.blit(text, text_rect)
        
    def draw_player_stats(self, surface, font, stat_positions):
        stat_lines = {
            "coins": f"{self.coins}",
            "health": f"{self.health}",
            "damage": f"{self.damage:.2f}".rstrip("0").rstrip("."),
            "speed": f"{self.speed:.2f}".rstrip("0").rstrip("."),
            "fire_rate": f"{self.fire_rate:.2f}".rstrip("0").rstrip("."),
            "shoot_distance": f"{self.shoot_distance:.2f}".rstrip("0").rstrip("."),
            "body_damage": f"{self.body_damage:.2f}".rstrip("0").rstrip("."),
            "luck": f"{self.luck:.2f}".rstrip("0").rstrip("."), 
        }

        for stat_name, text_value in stat_lines.items():
            text = font.render(text_value, True, config.HUD_COLOR)
            cx, cy = stat_positions[stat_name]

            text_rect = text.get_rect()
            text_rect.x = cx - text_rect.width // 2
            text_rect.y = cy - text_rect.height // 2

            surface.blit(text, text_rect)

    def draw_player_items(self, surface, font):
        lines = [
        f"Coins: {self.coins}",
        ]

        x = 15
        y = 200
        line_height = 28

        for line in lines:
            text = font.render(line, True, config.HUD_COLOR)
            surface.blit(text, (x, y))
            y += line_height

    def apply_item(self, item):
        self.items.append(item.item_id)
        
        data = ITEM_DEFINITIONS[item.item_id]
        effect = data["effect"]

        if effect["type"] == "stat":
            stat = effect["stat"]
            amount = effect["amount"]
            setattr(self, stat, getattr(self, stat) + amount)

        elif effect["type"] == "stat_multiplier":
            stat = effect["stat"]
            multiplier = effect["multiplier"]
            setattr(self, stat, getattr(self, stat) * multiplier)

        elif effect["type"] == "set_shot":
            self.bullet_type = effect["value"]

    
    def draw(self, surface):
        if self.invulnerability_timer > 0:
            blink_speed = 0.12
            if int(self.invulnerability_timer / blink_speed) % 2 == 0:
                return

        self.visual.draw(surface, self.x, self.y)