from game.entities.enemies.shooter_enemy import ShooterEnemy
from game.rooms.room_data import get_random_normal_room
from game.screens.combat_screen import CombatScreen


class PlayScreen(CombatScreen):
    def __init__(self, game):
        super().__init__(game, get_random_normal_room(), "normal")
        self.spawn_room_enemies()

    def spawn_room_enemies(self):
        for enemy_pos in self.room.enemy_spawns:
            self.enemies.append(ShooterEnemy(enemy_pos))
