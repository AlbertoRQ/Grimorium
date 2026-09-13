"""A heavy pursuer with committed, telegraphed leaps and aimed volleys."""

import math

import pygame

from game import config
from game.entities.bosses.basic_boss import BasicBoss
from game.entities.bullets.bullet import Bullet
from game.entities.enemies.enemy import Enemy
from game.visuals.animated_visual import AnimatedVisual


class LeapingBoss(BasicBoss):
    def __init__(self, level=1):
        super().__init__(level)
        self.speed = self.base_speed = 38
        self.state = "pursue"
        self.state_time = 0.0
        self.attack_index = 0
        self.jump_height = 0.0
        self.contact_disabled = False
        self.target = pygame.Vector2(self.x, self.y)
        self.jump_start = self.target.copy()
        self.pending_shots = []
        self.visual = AnimatedVisual(
            image_folder="enemies/golem", image_name="golem.bmp",
            frame_cols=1, frame_rows=1, scale_x=96, scale_y=96,
            use_alpha=False, colorkey=(84, 206, 76),
            initial_state="idle", initial_facing="down",
            animations={"idle": {"row": 0, "frames": [0], "speed": .25, "loop": True}},
        )

    def enter(self, state):
        self.state = state
        self.state_time = 0.0

    def apply_knockback(self, dir_x, dir_y, strength):
        if self.state != "jump":
            super().apply_knockback(dir_x, dir_y, strength * .15)

    def lock_jump_target(self, player, blockers):
        start = pygame.Vector2(self.x, self.y)
        delta = pygame.Vector2(player.x, player.y) - start
        if delta.length() > 180:
            delta.scale_to_length(180)
        # Trace the whole route so leaps never finish in, or tunnel through, walls.
        self.target = start.copy()
        steps = max(1, math.ceil(delta.length() / 4))
        for step in range(1, steps + 1):
            candidate = start + delta * (step / steps)
            self.x, self.y = candidate
            if self.collides_with_rects(blockers):
                break
            self.target = candidate
        self.x, self.y = start

    def volley(self, player, room):
        direction = pygame.Vector2(player.x - self.x, player.y - self.y)
        if not direction.length_squared():
            direction = pygame.Vector2(0, 1)
        direction = direction.normalize()
        for index in range(7):
            velocity = direction.rotate((index - 3) * 13) * (115 + (index % 2) * 15)
            self.pending_shots.append(Bullet(
                self.x, self.y, velocity.x, velocity.y,
                config.ENEMY_BULLET_COLOR, 4, self.damage, 1, 900,
                world_width=getattr(room, "viewport_width", config.SCREEN_WIDTH),
                world_height=getattr(room, "viewport_height", config.SCREEN_HEIGHT),
            ))

    def move(self, player, dt, blockers, entities, room=None):
        if self.is_dead():
            return
        if self.status_effects["ice"]["ice_timer"] > 0:
            self.jump_height = 0
            self.contact_disabled = False
            self.enter("recover")
            return
        self.state_time += dt
        if self.state == "pursue":
            Enemy.move(self, player, min(dt, .05), blockers, entities, room)
            if self.state_time >= 1.1:
                self.attack_index += 1
                if self.attack_index % 3 == 0:
                    self.enter("spit_warning")
                else:
                    self.lock_jump_target(player, blockers)
                    self.enter("jump_warning")
        elif self.state == "jump_warning":
            if self.state_time >= .65:
                self.jump_start = pygame.Vector2(self.x, self.y)
                self.knockback_x = self.knockback_y = 0
                self.enter("jump")
                self.contact_disabled = True
        elif self.state == "jump":
            progress = min(1, self.state_time / .7)
            destination = self.jump_start.lerp(self.target, progress)
            delta = destination - pygame.Vector2(self.x, self.y)
            steps = max(1, math.ceil(delta.length() / 4))
            for _ in range(steps):
                self.move_by(delta.x / steps, delta.y / steps, blockers, entities)
            self.jump_height = math.sin(progress * math.pi) * 50
            if progress >= 1:
                self.jump_height = 0
                self.contact_disabled = False
                self.enter("recover")
        elif self.state == "spit_warning":
            if self.state_time >= .7:
                self.volley(player, room)
                self.enter("recover")
        elif self.state == "recover" and self.state_time >= .85:
            self.enter("pursue")

    def update(self, player, dt, blockers, entities, room=None):
        # Use the normal status system without the test boss's regeneration.
        self.pending_shots = []
        Enemy.update(self, player, dt, blockers, entities, room)
        return self.pending_shots

    def draw_ground_shadow(self, surface):
        pygame.draw.ellipse(surface, (38, 33, 43),
                            (round(self.x - 23), round(self.y + 18), 46, 12))
        if self.state in ("jump_warning", "jump"):
            pygame.draw.circle(surface, (210, 135, 72),
                               (round(self.target.x), round(self.target.y)), self.radius, 1)

    def draw(self, surface):
        if self.state in ("jump_warning", "spit_warning"):
            pulse = math.sin(self.state_time * 18)
            self.visual.set_size(100 + round(pulse * 2), 90)
        elif self.state == "recover" and self.state_time < .2:
            self.visual.set_size(104, 86)
        else:
            self.visual.set_size(96, 96)
        Enemy.draw(self, surface, -round(self.jump_height))
        if self.state == "spit_warning":
            pygame.draw.circle(surface, (245, 143, 82),
                               (round(self.x), round(self.y + 12)), 5, 1)
