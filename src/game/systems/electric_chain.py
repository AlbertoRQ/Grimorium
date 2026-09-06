import math
import random
import pygame


class ElectricChain:
    def __init__(
        self,
        source,
        damage,
        max_jumps,
        max_jump_distance,
        jump_duration=0.15,
        can_second_discharge=False,
        is_second_discharge=False,
    ):
        self.source = source
        self.target = None

        self.damage = damage
        self.max_jumps = max_jumps
        self.jumps_done = 0
        self.max_jump_distance = max_jump_distance

        self.jump_duration = jump_duration
        self.timer = 0
        self.can_second_discharge = can_second_discharge
        self.is_second_discharge = is_second_discharge

        self.visited = {source}
        self.finished = False

    def create_second_discharge(self):
        if not self.can_second_discharge or self.is_second_discharge:
            return []

        return [
            ElectricChain(
                source=self.source,
                damage=self.damage,
                max_jumps=self.max_jumps,
                max_jump_distance=self.max_jump_distance,
                jump_duration=self.jump_duration,
                can_second_discharge=False,
                is_second_discharge=True,
            )
        ]

    def find_next_target(self, enemies):
        possible_targets = []

        for enemy in enemies:
            if enemy in self.visited or enemy.is_dead():
                continue

            distance = math.hypot(
                enemy.x - self.source.x,
                enemy.y - self.source.y,
            )

            if distance <= self.max_jump_distance:
                possible_targets.append(enemy)

        if not possible_targets:
            return None

        return min(
            possible_targets,
            key=lambda enemy: math.hypot(
                enemy.x - self.source.x,
                enemy.y - self.source.y,
            ),
        )

    def update(self, dt, enemies):
        if self.finished:
            return []

        if self.target is None:
            self.target = self.find_next_target(enemies)

            if self.target is None:
                self.finished = True
                return self.create_second_discharge()

        self.timer += dt

        if self.timer >= self.jump_duration:
            self.target.take_damage(self.damage)

            self.visited.add(self.target)
            self.source = self.target
            self.target = None

            self.jumps_done += 1
            self.timer = 0

            if self.jumps_done >= self.max_jumps:
                self.finished = True
                return self.create_second_discharge()

        return []


    def draw(self, surface):
        if self.finished or self.target is None:
            return

        progress = min(self.timer / self.jump_duration, 1)

        start_x = self.source.x
        start_y = self.source.y

        end_x = start_x + (self.target.x - start_x) * progress
        end_y = start_y + (self.target.y - start_y) * progress

        dx = end_x - start_x
        dy = end_y - start_y
        length = math.hypot(dx, dy)

        if length == 0:
            return

        perpendicular_x = -dy / length
        perpendicular_y = dx / length

        points = [(start_x, start_y)]

        segment_length = 8
        segments = max(1, math.ceil(length / segment_length))
        max_offset = min(6, length * 0.15)

        for index in range(1, segments):
            amount = index / segments
            offset = random.uniform(-max_offset, max_offset)

            x = start_x + dx * amount + perpendicular_x * offset
            y = start_y + dy * amount + perpendicular_y * offset

            points.append((x, y))

        points.append((end_x, end_y))

        outer_color = (255, 233, 59)
        inner_color = (255, 253, 253)

        pygame.draw.lines(surface, outer_color, False, points, 3)
        pygame.draw.lines(surface, inner_color, False, points, 1)
