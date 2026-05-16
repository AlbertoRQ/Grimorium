"""Enemigo lento pero muy resistente."""

from game import config
from game.entities.enemies.enemy import Enemy


class TankEnemy(Enemy):
    def __init__(self, position):
        super().__init__(
            position=position,
            speed=config.TANK_ENEMY_SPEED,
            max_health=config.TANK_ENEMY_MAX_HEALTH,
            radius=config.TANK_ENEMY_RADIUS,
            color=config.ENEMY_COLOR,
            damage=config.ENEMY_DAMAGE,
            score_value=35,
        )
