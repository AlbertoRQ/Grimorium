"""Jugador sencillo, basado en la version que ya tenias clara."""

import math
import pygame

from game import config
from game.entities.entity import LivingEntity
from game.systems.shot_builder import build_player_shot
from game.visuals.animated_visual import AnimatedVisual


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
        self.shot_modifiers = set()

        self.base_bullet_elements = []
        # self.extra_bullet_element = {"poison":1, "ice":1, "electric":1}
        self.extra_bullet_element = {}
        self.power_element_order = []
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
            "electric": {
                "level": 1,
                "damage_percentage": 0.40,
                "max_targets": 2,
                "max_jump_distance": 100,
            },
            "poison": {
                "level": 1,
                "max_stacks": 5,
                "damage_taken_per_stack": 0.05,
                "boss_duration": 2,
            },
        }
        
        self.combo_stats = {
            "fire_ice": {
                "level": 1,
                "damage_multiplier": 2.0,
            },
            "fire_electric": {
                "level": 1,
                "fragment_count": 5,
                "damage_multiplier": 0.50,
                "fragment_range": 60,
                "embed_duration": 1,
                "spread_angle": 80,
            },
            "ice_electric": {
                "level": 1,
                "puddle_size_multiplier": 1.0,
                "puddle_duration_bonus": 1.0,
                "electric_duration": 2.0,
                "tick_damage": 0.5,
            },
            "fire_poison": {
                "level": 1,
                "cloud_radius": 35,
                "cloud_duration": 3.0,
                "tick_time": 0.75,
                "stacks_per_tick": 1,
            },
            "ice_poison": {
                "level": 1,
                "fragile_duration": 3.0,
                "execute_base_threshold": 0.03,
                "execute_threshold_per_stack": 0.02,
            },
        }

        self.invulnerability_timer = 0

        self.coins = config.PLAYER_COINS

        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 667
        self.friction = 667

        self.speed_animation = 0.20

        self.visual = AnimatedVisual(
            image_folder="player",
            image_name="mage_animated.png",
            frame_cols=4,
            frame_rows=4,
            scale_x = 32,
            scale_y = 32,
            use_alpha=True,
            initial_state="idle",
            initial_facing="down",
            animations={
                "idle_right": {"row": 0, "frames": [0], "speed": self.speed_animation, "loop": True},
                "walk_right": {"row": 0, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},

                "idle_left": {"row": 1, "frames": [0], "speed": self.speed_animation, "loop": True},
                "walk_left": {"row": 1, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},

                "idle_down": {"row": 2, "frames": [0], "speed": self.speed_animation, "loop": True},
                "walk_down": {"row": 2, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},

                "idle_up": {"row": 3, "frames": [0], "speed": self.speed_animation, "loop": True},
                "walk_up": {"row": 3, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},
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
        if speed > self.speed:
            scale = self.speed / speed
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

        speed_factor = move_speed / self.speed
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

        bullets, cooldown_multiplier = build_player_shot(
            self,
            vel_x,
            vel_y,
        )

        self.shoot_timer = self.fire_rate * cooldown_multiplier
        return bullets


    
    def draw_player_health(self, surface, font):

        bar_width = 120
        bar_height = 16

        x = 25
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

    
    def draw(self, surface):
        if self.invulnerability_timer > 0:
            blink_speed = 0.12
            if int(self.invulnerability_timer / blink_speed) % 2 == 0:
                return

        self.visual.draw(surface, self.x, self.y)
