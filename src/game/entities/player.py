"""Jugador sencillo, basado en la version que ya tenias clara."""

import math
import pygame
import random

from game import config
from game.entities.entity import LivingEntity
from game.entities.bullets.bullet import create_normal_shot
from game.entities.bullets.bullet import create_gatling_shot
from game.entities.bullets.bullet import create_spread_shot
from game.entities.items.item_data import ITEM_DEFINITIONS 

from game.utils.paths import asset_path

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
                "level": 1,
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

        self.sprite_sheet = pygame.image.load(asset_path("images", "player", "mage2.bmp")).convert()
        self.sprite_sheet .set_colorkey((35, 97, 72))
        self.frame_cols = 4
        self.frame_rows = 1

        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()

        self.frame_width = sheet_width // self.frame_cols
        self.frame_height = sheet_height // self.frame_rows

        self.sprite_size_x = self.radius * 3
        self.sprite_size_y = self.radius * 3

        self.sprite = self.get_frame(2, 0)
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite_size_x, self.sprite_size_y))



    def move(self, keys, dt, blockers, entities):
        move_x = 0
        move_y = 0

        if keys[pygame.K_d]:
            move_x += 1
            self.sprite = self.get_frame(1, 0)
        if keys[pygame.K_a]:
            move_x -= 1
            self.sprite = self.get_frame(0, 0)
        if keys[pygame.K_w]:
            move_y -= 1
            self.sprite = self.get_frame(3, 0)
        if keys[pygame.K_s]:
            move_y += 1
            self.sprite = self.get_frame(2, 0)

        length = math.hypot(move_x, move_y)
        if length > 0:
            move_x /= length
            move_y /= length

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
        
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite_size_x, self.sprite_size_y))

    def update(self, dt):
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if self.invulnerability_timer > 0:
            self.color = config.PLAYER_COLOR_INVENCIBLE
            self.invulnerability_timer -= dt
        
        if self.invulnerability_timer <= 0:
            self.color = config.PLAYER_COLOR

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
        
    def draw_player_stats(self, surface, font, x=15, y=200):
        lines = [
        f"Coins: {self.coins}",
        f"Health: {self.health}",
        f"Damage: {self.damage}",
        f"Speed: {self.speed}",
        f"Fire rate: {self.fire_rate}",
        f"Shoot distance: {self.shoot_distance}",
        f"Body damage: {self.body_damage}",
        f"Luck: {self.luck}",
        f"Base elements: {self.base_bullet_elements}",
        f"Extra elements: {self.extra_bullet_element}",
        f"Fire lvl: {self.element_stats['fire']['level']}",
        f"Ice lvl: {self.element_stats['ice']['level']}",
        ]

        line_height = 28

        for line in lines:
            text = font.render(line, True, config.HUD_COLOR)
            surface.blit(text, (x, y))
            y += line_height

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

    def get_frame(self, col, row):
        frame_rect = pygame.Rect(
            col * self.frame_width,
            row * self.frame_height,
            self.frame_width,
            self.frame_height,
        )
        return self.sprite_sheet.subsurface(frame_rect).copy()

    def draw(self, surface):
        sprite_rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.sprite, sprite_rect)