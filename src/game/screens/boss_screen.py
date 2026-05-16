from game.entities.bosses.basic_boss import BasicBoss
from game.rooms.room_data import get_random_boss_room
from game.screens.combat_screen import CombatScreen


class BossScreen(CombatScreen):
    def __init__(self, game):
        super().__init__(game, get_random_boss_room(), "boss")

        self.boss = BasicBoss()

        if self.room.boss_spawn is not None:
            self.boss.x, self.boss.y = self.room.boss_spawn

        self.enemies = [self.boss]

    def draw_extra(self, surface):
        if not self.boss.is_dead():
            self.boss.draw_boss_health_bar(surface, self.font)
