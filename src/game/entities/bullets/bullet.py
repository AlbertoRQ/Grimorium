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
        elements=None,
        effect_data=None,
        world_width=None,
        world_height=None,
    ):
        super().__init__(x, y, radius, color)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = damage
        self.rate = rate
        self.max_distance = max_distance
        self.distance_traveled = 0
        self.destroyed = False

        self.elements = elements or []
        self.effect_data = effect_data or {}

        self.world_width = world_width
        self.world_height = world_height

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
        world_width = self.world_width if self.world_width is not None else config.SCREEN_WIDTH
        world_height = self.world_height if self.world_height is not None else config.SCREEN_HEIGHT

        return (
            self.x > world_width + self.radius
            or self.x < -self.radius
            or self.y > world_height + self.radius
            or self.y < -self.radius
        )
    
    def draw(self, surface):
        if "ice" in self.elements:
            pygame.draw.circle(surface, (120, 200, 255), (int(self.x), int(self.y)), self.radius + 4)

        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)




BULLET_TYPES = {
    "normal": {
        "radius": config.BULLET_RADIUS,
        "damage": config.BULLET_DAMAGE,
        "rate": 1,
    },
    "gatling": {
        "radius": config.BULLET_RADIUS*0.75,
        "damage": config.BULLET_DAMAGE,
        "rate": 0.5,
    },
    "spread": {
        "radius": config.BULLET_RADIUS*1.5,
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




def build_bullet(x, y, vel_x, vel_y, max_dist, bullet_type, bullet_elements, effect_data):
    data = BULLET_TYPES[bullet_type]
    main_element = bullet_elements[0] if bullet_elements else None
    color = ELEMENT_COLORS[main_element]
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
        elements = bullet_elements,
        effect_data=effect_data,
    )

def create_normal_shot(x, y, vel_x, vel_y, max_dist, elements, effect_data):
    bullet = build_bullet(x, y, vel_x, vel_y, max_dist, "normal", elements, effect_data)
    return [bullet], bullet.rate

def create_gatling_shot(x, y, vel_x, vel_y, max_dist, elements, effect_data):
    bullet = build_bullet(x, y, vel_x, vel_y, max_dist, "gatling", elements, effect_data)
    return [bullet], bullet.rate

def create_spread_shot(x, y, vel_x, vel_y, max_dist, elements, effect_data):
    bullets = []
    base_velocity = pygame.Vector2(vel_x, vel_y)
    
    total = 3
    angle_step = 12
    middle_index = (total - 1) / 2

    for index in range(total):
        angle = (index - middle_index) * angle_step
        rotated_velocity = base_velocity.rotate(angle)
        bullets.append(build_bullet(x, y, rotated_velocity.x, rotated_velocity.y, max_dist, "spread", elements, effect_data))

    return bullets, bullets[0].rate


