"""Enemigo que intenta disparar al jugador."""

import math

from game import config
from game.entities.bullets.bullet import create_normal_shot
from game.entities.enemies.enemy import Enemy


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

    def move(self, player, dt, blockers, circle):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance <= 0:
            return

        direction = 0

        if distance > self.preferred_distance:
            direction = 1
        elif distance < self.preferred_distance - 50:
            direction = -1

        if direction == 0:
            return

        move_x = direction * (diff_x / distance) * self.speed * dt
        move_y = direction * (diff_y / distance) * self.speed * dt

        self.move_by(move_x, move_y, blockers, circle)

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
