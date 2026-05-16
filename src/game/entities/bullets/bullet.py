"""Bala base."""

from game import config
from game.entities.entity import Entity


class Bullet(Entity):
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__(x, y, config.BULLET_RADIUS, config.BULLET_COLOR)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = config.BULLET_DAMAGE
        self.rate = config.BULLET_RATE
        self.speed = config.BULLET_SPEED

    def update(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def is_offscreen(self):
        return (
            self.x > config.SCREEN_WIDTH + self.radius
            or self.x < -self.radius
            or self.y > config.SCREEN_HEIGHT + self.radius
            or self.y < -self.radius
        )
