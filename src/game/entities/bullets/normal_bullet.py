"""Bala simple y directa."""

from game.entities.bullets.bullet import Bullet


class NormalBullet(Bullet):
    """Por ahora se comporta como la bala base."""


def create_normal_shot(x, y, vel_x, vel_y):
    bullet = NormalBullet(x, y, vel_x, vel_y)
    return [bullet], bullet.rate
