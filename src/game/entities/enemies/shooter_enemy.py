"""Enemigo que intenta disparar al jugador."""

import math

from game import config
from game.entities.bullets.bullet import create_normal_shot
from game.entities.enemies.enemy import Enemy
from game.visuals.animated_visual import AnimatedVisual


class ShooterEnemy(Enemy):
    def __init__(self, position):
        super().__init__(
            position=position,
            speed=config.SHOOTER_ENEMY_SPEED,
            max_health=config.ENEMY_MAX_HEALTH,
            radius=config.SHOOTER_ENEMY_RADIUS,
            color=config.SHOOTER_ENEMY_COLOR,
            damage=config.ENEMY_DAMAGE,
            score_value=20,
        )
        self.shoot_cooldown = config.SHOOTER_ENEMY_FIRE_COOLDOWN
        self.bullet_speed = config.SHOOTER_ENEMY_BULLET_SPEED
        self.shoot_timer = 0.0
        self.preferred_distance = 300
        self.shoot_distance = config.SHOOTER_ENEMY_SHOOT_DISTANCE
        self.bullet_element = None

        self.visual = AnimatedVisual(
            image_folder="enemies/rat",
            image_name="rat_animated.png",
            frame_cols=4,
            frame_rows=4,
            scale_x=self.radius * 5,
            scale_y=self.radius * 5,
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


    def move(self, player, dt, blockers, entities):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance <= 0:
            self.visual.set_state("idle")
            return

        direction = 0

        if distance > self.preferred_distance:
            direction = 1
        elif distance < self.preferred_distance - 50:
            direction = -1

        if direction == 0:
            self.visual.set_state("idle")
            return

        move_x = direction * (diff_x / distance) * self.speed * dt
        move_y = direction * (diff_y / distance) * self.speed * dt

        old_x = self.x
        old_y = self.y

        self.move_by(move_x, move_y, blockers, entities)

        real_move_x = self.x - old_x
        real_move_y = self.y - old_y

        self.update_visual_from_movement(real_move_x, real_move_y)

    def shoot(self, player):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance >= self.preferred_distance or self.shoot_timer > 0:
            return []

        if distance <= 0:
            return []

        vel_x = (diff_x / distance) * self.bullet_speed
        vel_y = (diff_y / distance) * self.bullet_speed


        effect_data = {}
        if self.bullet_element is not None:
            effect_data = self.element_stats[self.bullet_element].copy()
        shot, rate = create_normal_shot(self.x, self.y, vel_x, vel_y, self.shoot_distance, self.bullet_element, effect_data)
        self.shoot_timer = self.shoot_cooldown * rate
        for bullet in shot:
            bullet.color = config.ENEMY_BULLET_COLOR

        return shot

    def update(self, player, dt, blockers, entities):
        super().update(player, dt, blockers, entities)
        self.shoot_timer = max(0, self.shoot_timer - dt)
        return self.shoot(player)
