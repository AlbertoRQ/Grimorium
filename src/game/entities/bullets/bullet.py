"""Bala base."""

import pygame
import math
from game import config
from game.entities.entity import Entity



class Bullet(Entity):
    def __init__(
        self,
        x,
        y,
        vel_x,
        vel_y,
        color,
        radius,
        damage,
        rate,
        max_distance,
        element=None,
        effect_data=None,
    ):
        super().__init__(x, y, radius, color)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = damage
        self.rate = rate
        self.max_distance = max_distance
        self.distance_traveled = 0
        self.destroyed = False

        self.element = element
        self.effect_data = effect_data or {}

    def update(self, dt, blockers):
        move_x = self.vel_x * dt
        move_y = self.vel_y * dt
        step_distance = math.hypot(move_x, move_y)

        self.x += move_x
        self.y += move_y

        self.distance_traveled += step_distance

        if self.distance_traveled >= self.max_distance:
            self.destroyed = True

        if self.collides_with_rects(blockers):
            self.destroyed = True

    def is_offscreen(self):
        return (
            self.x > config.SCREEN_WIDTH + self.radius
            or self.x < -self.radius
            or self.y > config.SCREEN_HEIGHT + self.radius
            or self.y < -self.radius
        )




BULLET_TYPES = {
    "normal": {
        "radius": config.BULLET_RADIUS,
        "damage": config.BULLET_DAMAGE,
        "rate": 1,
    },
    "gatling": {
        "radius": 5,
        "damage": config.BULLET_DAMAGE,
        "rate": 0.5,
    },
    "spread": {
        "radius": 15,
        "damage": config.BULLET_DAMAGE,
        "rate": 2,
    },
}

ELEMENT_COLORS = {
    None: (218, 245, 244),
    "fire": (255, 137, 69),
    "ice": (64, 202, 255),
    "electric": (235, 214, 75),
}




def build_bullet(x, y, vel_x, vel_y, max_dist, bullet_type, bullet_element, effect_data):
    data = BULLET_TYPES[bullet_type]
    color = ELEMENT_COLORS[bullet_element]
    return Bullet(
        x=x,
        y=y,
        vel_x=vel_x,
        vel_y=vel_y,
        color=color,
        radius=data["radius"],
        damage=data["damage"],
        rate=data["rate"],
        max_distance=max_dist,
        element = bullet_element,
        effect_data=effect_data,
    )

def create_normal_shot(x, y, vel_x, vel_y, max_dist, element, effect_data):
    bullet = build_bullet(x, y, vel_x, vel_y, max_dist, "normal", element, effect_data)
    return [bullet], bullet.rate

def create_gatling_shot(x, y, vel_x, vel_y, max_dist, element, effect_data):
    bullet = build_bullet(x, y, vel_x, vel_y, max_dist, "gatling", element, effect_data)
    return [bullet], bullet.rate

def create_spread_shot(x, y, vel_x, vel_y, max_dist, element, effect_data):
    bullets = []
    base_velocity = pygame.Vector2(vel_x, vel_y)
    
    total = 3
    angle_step = 12
    middle_index = (total - 1) / 2

    for index in range(total):
        angle = (index - middle_index) * angle_step
        rotated_velocity = base_velocity.rotate(angle)
        bullets.append(build_bullet(x, y, rotated_velocity.x, rotated_velocity.y, max_dist, "spread", element, effect_data))

    return bullets, bullets[0].rate