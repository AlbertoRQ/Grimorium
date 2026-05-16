"""Bala metralleta."""

from game.entities.bullets.bullet import Bullet


class GatlingBullet(Bullet):
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__(x, y, vel_x, vel_y)
        self.color = (0, 200, 255)
        self.radius = 5
        self.rate = 0.5


def create_gatling_shot(x, y, vel_x, vel_y):
    bullet = GatlingBullet(x, y, vel_x, vel_y)
    return [bullet], bullet.rate
