import math
import random
import pygame


class ToxicOverload:
    def __init__(self, player, combo_data):
        self.player = player

        self.radius = combo_data["radius"]
        self.drain_per_second = combo_data["drain_per_second"]
        #self.drain_per_second = max(0.12, combo_data["drain_per_second"])
        self.speed_multiplier = combo_data["speed_multiplier"]
        self.tick_time = combo_data["tick_time"]
        self.tick_damage = combo_data["tick_damage"]
        self.charge_decay_factor = combo_data["charge_decay_factor"]

        self.charge = 1.0
        self.max_charge = 1.0
        self.tick_timer = 0
        self.fed_enemies = set()
        self.finished = False

    def update(self, dt, enemies):
        if self.finished:
            return

        self.feed_new_enemies(enemies)

        self.charge = max(0, self.charge - self.drain_per_second * dt)

        self.tick_timer -= dt
        if self.tick_timer <= 0:
            self.damage_enemies(enemies)
            self.tick_timer = self.tick_time

        if self.charge <= 0:
            self.finished = True

    def feed_new_enemies(self, enemies):
        for enemy in enemies:
            if enemy.is_dead() or enemy in self.fed_enemies:
                continue

            distance = math.hypot(
                enemy.x - self.player.x,
                enemy.y - self.player.y,
            )

            if distance <= self.radius + enemy.radius:
                max_charge = (
                    self.charge_decay_factor
                    ** len(self.fed_enemies)
                )

                self.max_charge = max_charge
                self.charge = self.max_charge
                self.fed_enemies.add(enemy)

    def damage_enemies(self, enemies):
        for enemy in enemies:
            if enemy.is_dead():
                continue

            distance = math.hypot(
                enemy.x - self.player.x,
                enemy.y - self.player.y,
            )

            if distance <= self.radius + enemy.radius:
                enemy.take_damage(self.tick_damage)

    def draw(self, surface):
        if self.finished:
            return

        center = (int(self.player.x), int(self.player.y))

        field_width = self.radius * 2
        field_height = int(self.radius * 1.6)
        field_surface = pygame.Surface(
            (field_width, field_height),
            pygame.SRCALPHA,
        )
        field_rect = (0, 0, field_width, field_height)

        # La elipse da al campo una sensación de cúpula sobre el suelo.
        pygame.draw.ellipse(field_surface, (205, 145, 230, 80), field_rect)
        self.draw_electric_sparks(field_surface)

        pygame.draw.ellipse(
            field_surface,
            (255, 220, 70, 185),
            field_rect,
            2,
        )

        surface.blit(
            field_surface,
            (center[0] - self.radius, center[1] - field_height // 2),
        )

        bar_width = 34
        bar_height = 4
        bar_x = center[0] - bar_width // 2
        bar_y = center[1] - self.player.radius - 12

        pygame.draw.rect(
            surface,
            (35, 35, 35),
            (bar_x, bar_y, bar_width, bar_height),
        )

        pygame.draw.rect(
            surface,
            (190, 120, 220),
            (
                bar_x,
                bar_y,
                int(bar_width * (self.charge / self.max_charge)),
                bar_height,
            ),
        )

        pygame.draw.rect(
            surface,
            (255, 235, 135),
            (bar_x, bar_y, bar_width, bar_height),
            1,
        )

    def draw_electric_sparks(self, field_surface):
        frame = pygame.time.get_ticks() // 65
        rng = random.Random(frame)
        center = pygame.Vector2(
            field_surface.get_width() / 2,
            field_surface.get_height() / 2,
        )
        radius_x = field_surface.get_width() / 2
        radius_y = field_surface.get_height() / 2

        for _ in range(4):
            bolt_angle = rng.uniform(0, math.tau)
            start_distance = rng.uniform(1, self.radius * 0.08)
            start = pygame.Vector2(
                center.x + math.cos(bolt_angle) * start_distance,
                center.y + math.sin(bolt_angle) * start_distance,
            )

            edge_distance = rng.uniform(0.58, 0.9)
            end = pygame.Vector2(
                center.x + math.cos(bolt_angle) * radius_x * edge_distance,
                center.y + math.sin(bolt_angle) * radius_y * edge_distance,
            )

            direction = end - start
            normal = pygame.Vector2(-direction.y, direction.x).normalize()
            middle = start.lerp(end, 0.5) + normal * rng.uniform(-4, 4)
            points = [
                (int(start.x), int(start.y)),
                (int(middle.x), int(middle.y)),
                (int(end.x), int(end.y)),
            ]

            pygame.draw.lines(field_surface, (255, 210, 55, 195), False, points, 2)
            pygame.draw.lines(field_surface, (255, 250, 190, 230), False, points, 1)
