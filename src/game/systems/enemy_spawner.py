"""Crea enemigos a lo largo de la partida."""

import random

from game import config
from game.entities.enemies.chaser_enemy import ChaserEnemy
from game.entities.enemies.shooter_enemy import ShooterEnemy
from game.entities.enemies.tank_enemy import TankEnemy


class EnemySpawner:
    def __init__(self):
        self.timer = 0.0

    def update(self, dt, wave_number):
        """Devuelve una lista de enemigos nuevos para este frame."""
        spawned_enemies = []
        self.timer -= dt

        if self.timer <= 0:
            spawned_enemies.append(self.spawn_enemy(wave_number))

            # Cuanto mayor sea la oleada, mas rapido aparecen.
            next_interval = config.SPAWN_INTERVAL - (wave_number - 1) * 0.08
            self.timer = max(0.45, next_interval)

        return spawned_enemies

    def spawn_enemy(self, wave_number):
        position = self._random_edge_position()

        # Reglas simples para empezar.
        if wave_number >= 5 and random.random() < 0.2:
            return TankEnemy(position)

        if wave_number >= 3 and random.random() < 0.3:
            return ShooterEnemy(position)

        return ChaserEnemy(position)

    def _random_edge_position(self):
        edge = random.choice(["top", "bottom", "left", "right"])

        if edge == "top":
            return random.randint(0, config.SCREEN_WIDTH), -30
        if edge == "bottom":
            return random.randint(0, config.SCREEN_WIDTH), config.SCREEN_HEIGHT + 30
        if edge == "left":
            return -30, random.randint(0, config.SCREEN_HEIGHT)

        return config.SCREEN_WIDTH + 30, random.randint(0, config.SCREEN_HEIGHT)
