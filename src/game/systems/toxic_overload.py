import math
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

        field_surface = pygame.Surface(
            (self.radius * 2, self.radius * 2),
            pygame.SRCALPHA,
        )

        pygame.draw.circle(
            field_surface,
            (110, 220, 70, 55),
            (self.radius, self.radius),
            self.radius,
        )

        pygame.draw.circle(
            field_surface,
            (225, 255, 70, 180),
            (self.radius, self.radius),
            self.radius,
            2,
        )

        surface.blit(
            field_surface,
            (center[0] - self.radius, center[1] - self.radius),
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
            (130, 240, 70),
            (
                bar_x,
                bar_y,
                int(bar_width * (self.charge / self.max_charge)),
                bar_height,
            ),
        )

        pygame.draw.rect(
            surface,
            (245, 255, 170),
            (bar_x, bar_y, bar_width, bar_height),
            1,
        )