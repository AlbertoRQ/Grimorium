"""Enemigo basico que solo persigue al jugador."""

import math
import random
import pygame

from game import config
from game.entities.enemies.enemy import Enemy
from game.systems.pathfinding import find_path


class ChaserEnemy(Enemy):
    def __init__(self, position, level=1):
        health = int(config.ENEMY_MAX_HEALTH * (1.12 ** (level-1)))
        #damage = int(config.ENEMY_DAMAGE * (1.08 ** (level - 1)))
        #speed = config.ENEMY_SPEED * (1.02 * (level - 1))

        super().__init__(
            position=position,
            speed=config.ENEMY_SPEED,
            max_health=health,
            radius=config.ENEMY_RADIUS,
            color=config.ENEMY_COLOR,
            damage=config.ENEMY_DAMAGE,
            score_value=10,
        )


        self.detection_distance = 300

        self.random_dir_x = 0
        self.random_dir_y = 0
        self.random_move_timer = 0
        self.random_move_interval = 1.5

        self.path = []
        self.path_timer = 0
        self.path_recalculate_interval = 0.3
        self.path_target_cell = None


    def choose_random_direction(self):
        self.random_dir_x = random.uniform(-1, 1)
        self.random_dir_y = random.uniform(-1, 1)

        length = math.hypot(self.random_dir_x, self.random_dir_y)

        if length > 0:
            self.random_dir_x /= length
            self.random_dir_y /= length


    def move(self, player, dt, blockers, entities, room=None):
        diff_x = player.x - self.x
        diff_y = player.y - self.y
        distance = math.hypot(diff_x, diff_y)

        if distance <= 0:
            return

        if distance <= self.detection_distance and not player.invulnerability_timer > 0:
            if room is not None:
                move_x, move_y = self.get_path_movement(player, dt, room, blockers)
            else:
                move_x = (diff_x / distance) * self.speed * dt
                move_y = (diff_y / distance) * self.speed * dt
        else:
            self.random_move_timer -= dt

            if self.random_move_timer <= 0:
                self.choose_random_direction()
                self.random_move_timer = self.random_move_interval

            move_x = self.random_dir_x * self.speed * dt
            move_y = self.random_dir_y * self.speed * dt

        old_x = self.x
        old_y = self.y

        other_entities = [entity for entity in entities if entity is not self]
        self.move_by(move_x, move_y, blockers, other_entities)

        real_move_x = self.x - old_x
        real_move_y = self.y - old_y

        self.update_visual_from_movement(real_move_x, real_move_y)
        
    
    def has_clear_path(self, start_x, start_y, target_x, target_y, blockers):
        steps = int(math.hypot(target_x - start_x, target_y - start_y) / 4)

        if steps <= 0:
            return True

        old_x = self.x
        old_y = self.y

        for step in range(1, steps + 1):
            t = step / steps
            self.x = start_x + (target_x - start_x) * t
            self.y = start_y + (target_y - start_y) * t

            if self.collides_with_rects(blockers):
                self.x = old_x
                self.y = old_y
                return False

        self.x = old_x
        self.y = old_y
        return True

    
    def get_path_movement(self, player, dt, room, blockers):
        self.path_timer -= dt

        start_cell = room.world_to_cell(self.x, self.y)
        target_cell = room.world_to_cell(player.x, player.y)

        if self.path_timer <= 0 or target_cell != self.path_target_cell:
            self.path = find_path(room, start_cell, target_cell)
            self.path_timer = self.path_recalculate_interval
            self.path_target_cell = target_cell

        if len(self.path) <= 1:
            diff_x = player.x - self.x
            diff_y = player.y - self.y
        else:
            target_cell = self.path[1]

            for cell in self.path[2:]:
                target_x, target_y = room.cell_to_world(*cell)

                if self.has_clear_path(self.x, self.y, target_x, target_y, blockers):
                    target_cell = cell
                else:
                    break

            target_x, target_y = room.cell_to_world(*target_cell)

            diff_x = target_x - self.x
            diff_y = target_y - self.y

            if math.hypot(diff_x, diff_y) < getattr(self, "path_arrival_distance", 8):
                while len(self.path) > 1 and self.path[0] != target_cell:
                    self.path.pop(0)

                if len(self.path) > 1:
                    self.path.pop(0)

        length = math.hypot(diff_x, diff_y)

        if length <= 0:
            return 0, 0

        return (
            (diff_x / length) * self.speed * dt,
            (diff_y / length) * self.speed * dt,
        )