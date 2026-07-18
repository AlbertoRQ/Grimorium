import pygame
import random
import math


class IcePuddle:
    def __init__(self, x, y, enemy_radius, duration, combo_data):
        self.x = x
        self.y = y

        size_multiplier = combo_data["puddle_size_multiplier"]

        self.max_width = enemy_radius * 3.4 * size_multiplier
        self.max_height = enemy_radius * 2 * size_multiplier

        self.duration = duration
        self.timer = 0

        self.grow_duration = 0.20
        self.shrink_duration = 0.35

        self.finished = False
        self.electrified = False
        self.electric_timer = 0
        self.electric_duration = combo_data["electric_duration"]

        self.tick_timer = 0
        self.tick_interval = 0.35
        self.tick_damage = combo_data["tick_damage"]

    def electrify(self):
        self.electrified = True
        self.electric_timer = self.electric_duration

    def contains_entity(self, entity):
        scale = self.get_scale()

        if scale <= 0:
            return False

        width = self.max_width * scale
        height = self.max_height * scale

        radius_x = width / 2
        radius_y = height / 2

        entity_radius = getattr(entity, "radius", 0)

        radius_x += entity_radius
        radius_y += entity_radius

        if radius_x <= 0 or radius_y <= 0:
            return False

        dx = entity.x - self.x
        dy = entity.y - self.y

        ellipse_value = (
            (dx * dx) / (radius_x * radius_x)
            + (dy * dy) / (radius_y * radius_y)
        )

        return ellipse_value <= 1
    

    def update(self, dt, enemies=None):
        self.timer += dt

        if self.electrified:
            self.electric_timer -= dt
            self.tick_timer -= dt

            if self.tick_timer <= 0:
                self.damage_enemies(enemies or [])
                self.tick_timer = self.tick_interval

            if self.electric_timer <= 0:
                self.electrified = False
                self.electric_timer = 0

        if self.timer >= self.duration:
            self.finished = True

    def damage_enemies(self, enemies):
        for enemy in enemies:
            if enemy.is_dead():
                continue

            if self.contains_entity(enemy):
                enemy.take_damage(self.tick_damage)

    def get_scale(self):
        if self.timer < self.grow_duration:
            return self.timer / self.grow_duration

        time_left = self.duration - self.timer

        if time_left < self.shrink_duration:
            return max(0, time_left / self.shrink_duration)

        return 1

    def draw(self, surface):
        if self.finished:
            return

        scale = self.get_scale()

        if scale <= 0:
            return

        width = max(1, int(self.max_width * scale))
        height = max(1, int(self.max_height * scale))

        puddle_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.ellipse(
            puddle_surface,
            (70, 180, 230, 85),
            (0, 0, width, height),
        )

        pygame.draw.ellipse(
            puddle_surface,
            (190, 240, 255, 140),
            (0, 0, width, height),
            1,
        )

        draw_x = int(self.x - width / 2)
        draw_y = int(self.y - height / 2)

        if self.electrified:
            self.draw_electric_sparks(puddle_surface, width, height)

        surface.blit(puddle_surface, (draw_x, draw_y))


    def get_random_point_inside_ellipse(self, rng, center, radius_x, radius_y):
        angle = rng.uniform(0, math.tau)
        distance = math.sqrt(rng.uniform(0, 1))

        return pygame.Vector2(
            center.x + math.cos(angle) * radius_x * distance,
            center.y + math.sin(angle) * radius_y * distance,
        )


    def draw_electric_sparks(self, puddle_surface, width, height):
        frame = int(self.timer / 0.06)
        rng = random.Random(frame)

        spark_count = 3

        center = pygame.Vector2(width / 2, height / 2)
        radius_x = width / 2
        radius_y = height / 2

        max_bridge_length = min(width, height) * 0.45
        min_bridge_length = min(width, height) * 0.18

        for _ in range(spark_count):
            start = self.get_random_point_inside_ellipse(
                rng,
                center,
                radius_x,
                radius_y,
            )

            bridge_length = rng.uniform(
                min_bridge_length,
                max_bridge_length,
            )

            direction = rng.choice([-1, 1])

            end = pygame.Vector2(
                start.x + direction * bridge_length,
                start.y + rng.uniform(-7.5, 7.5),
            )

            dx_from_center = end.x - center.x
            dy_from_center = end.y - center.y

            ellipse_value = (
                (dx_from_center * dx_from_center) / (radius_x * radius_x)
                + (dy_from_center * dy_from_center) / (radius_y * radius_y)
            )

            if ellipse_value > 1:
                continue

            dx = end.x - start.x
            dy = end.y - start.y
            length = math.hypot(dx, dy)

            if length <= 0:
                continue

            arc_height = rng.uniform(2, 4)

            first_middle = pygame.Vector2(
                start.x + dx * 0.33,
                start.y + dy * 0.33 - arc_height,
            )

            second_middle = pygame.Vector2(
                start.x + dx * 0.66,
                start.y + dy * 0.66 - arc_height,
            )

            jitter = 2

            points = [
                (int(start.x), int(start.y)),
                (
                    int(first_middle.x + rng.uniform(-jitter, jitter)),
                    int(first_middle.y + rng.uniform(-jitter, jitter)),
                ),
                (
                    int(second_middle.x + rng.uniform(-jitter, jitter)),
                    int(second_middle.y + rng.uniform(-jitter, jitter)),
                ),
                (int(end.x), int(end.y)),
            ]

            pygame.draw.lines(
                puddle_surface,
                (255, 230, 70, 210),
                False,
                points,
                2,
            )

            pygame.draw.lines(
                puddle_surface,
                (255, 255, 240, 230),
                False,
                points,
                1,
            )