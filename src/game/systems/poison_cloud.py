import math
import pygame


class PoisonCloud:
    def __init__(self, x, y, combo_data, poison_data):
        self.x = x
        self.y = y

        self.radius = combo_data["cloud_radius"]
        self.duration = combo_data["cloud_duration"]
        self.tick_time = combo_data["tick_time"]
        self.tick_timer = 0

        self.stacks_per_tick = combo_data["stacks_per_tick"]
        self.poison_data = poison_data

        self.expired = False

    def update(self, dt, enemies):
        self.duration -= dt
        self.tick_timer -= dt

        if self.duration <= 0:
            self.expired = True
            return

        if self.tick_timer <= 0:
            self.apply_poison(enemies)
            self.tick_timer = self.tick_time

    def apply_poison(self, enemies):
        for enemy in enemies:
            if enemy.is_dead():
                continue

            distance = math.hypot(enemy.x - self.x, enemy.y - self.y)

            if distance <= self.radius + enemy.radius:
                poison = enemy.status_effects["poison"]

                poison["max_stacks"] = self.poison_data["max_stacks"]
                poison["damage_taken_per_stack"] = self.poison_data["damage_taken_per_stack"]

                poison["stacks"] = min(
                    poison["stacks"] + self.stacks_per_tick,
                    poison["max_stacks"],
                )

                if getattr(enemy, "is_boss", False):
                    poison["timer"] = self.poison_data["boss_duration"]

    def draw(self, surface):
        cloud_surface = pygame.Surface(
            (self.radius * 2, self.radius * 2),
            pygame.SRCALPHA,
        )

        pygame.draw.circle(
            cloud_surface,
            (170, 60, 220, 70),
            (self.radius, self.radius),
            self.radius,
        )

        pygame.draw.circle(
            cloud_surface,
            (210, 120, 255, 90),
            (self.radius, self.radius),
            self.radius,
            2,
        )

        surface.blit(
            cloud_surface,
            (self.x - self.radius, self.y - self.radius),
        )