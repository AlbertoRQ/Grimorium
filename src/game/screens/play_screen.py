from game.rooms.room_data import get_random_normal_room
from game.screens.combat_screen import CombatScreen

from random import choice
from game.entities.enemies.rat_enemy import RatEnemy
from game.entities.enemies.goblin_enemy import GoblinEnemy
from game.entities.enemies.golem_enemy import GolemEnemy
from game.entities.enemies.dragon_enemy import DragonEnemy


ENEMY_TYPES = [GoblinEnemy, GolemEnemy, DragonEnemy, RatEnemy]
#ENEMY_TYPES = [GolemEnemy]


class PlayScreen(CombatScreen):
    def __init__(self, game):
        super().__init__(game, get_random_normal_room(), "normal")
        self.spawn_room_enemies()

    def spawn_room_enemies(self):
        for enemy_pos in self.room.enemy_spawns:
            enemy_class = choice(ENEMY_TYPES)
            self.enemies.append(enemy_class(enemy_pos, self.game.enemy_level))
