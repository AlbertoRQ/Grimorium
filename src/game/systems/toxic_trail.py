import math

import pygame

from game.systems.effect_handlers import apply_poison_data


class ToxicTrail:
    """Rastro dañino que se deja durante Sobrecarga Tóxica."""

    def __init__(self, combo_data, effect_data):
        self.duration = combo_data["trail_duration"]
        self.radius = combo_data["trail_radius"]
        self.segment_spacing = combo_data["trail_segment_spacing"]
        self.tick_time = combo_data["trail_tick_time"]
        self.stacks_per_tick = combo_data["trail_stacks_per_tick"]
        self.poison_data = effect_data["poison"]
        self.ice_poison_data = effect_data["combos"]["ice_poison"]

        self.segments = []
        self.last_position = None
        self.tick_timer = 0

    @property
    def finished(self):
        return not self.segments

    def update(self, dt, enemies, player=None):
        if player is not None:
            self.leave_segments(player.x, player.y)
        else:
            self.last_position = None

        for segment in self.segments:
            segment["age"] += dt

        self.segments = [
            segment
            for segment in self.segments
            if segment["age"] < self.duration
        ]

        if not self.segments:
            return

        self.tick_timer -= dt
        if self.tick_timer <= 0:
            self.damage_enemies(enemies)
            self.tick_timer = self.tick_time

    def leave_segments(self, x, y):
        if self.last_position is None:
            self.last_position = (x, y)
            self.add_segment(x, y)
            return

        last_x, last_y = self.last_position
        distance = math.hypot(x - last_x, y - last_y)

        while distance >= self.segment_spacing:
            direction_x = (x - last_x) / distance
            direction_y = (y - last_y) / distance
            last_x += direction_x * self.segment_spacing
            last_y += direction_y * self.segment_spacing
            self.add_segment(last_x, last_y)
            distance = math.hypot(x - last_x, y - last_y)

        self.last_position = (last_x, last_y)

    def add_segment(self, x, y):
        self.segments.append({"x": x, "y": y, "age": 0})

    def damage_enemies(self, enemies):
        for enemy in enemies:
            if enemy.is_dead():
                continue

            for segment in self.segments:
                distance = math.hypot(
                    enemy.x - segment["x"],
                    enemy.y - segment["y"],
                )
                if distance <= self.radius + enemy.radius:
                    for _ in range(self.stacks_per_tick):
                        apply_poison_data(
                            enemy,
                            self.poison_data,
                            self.ice_poison_data,
                        )
                    break

    def draw(self, surface):
        for segment in self.segments:
            life_ratio = 1 - segment["age"] / self.duration
            alpha = int(95 * life_ratio)
            draw_radius = max(2, int(self.radius * (0.75 + life_ratio * 0.25)))
            trail_surface = pygame.Surface(
                (draw_radius * 2, draw_radius * 2),
                pygame.SRCALPHA,
            )

            pygame.draw.circle(
                trail_surface,
                (170, 85, 210, alpha),
                (draw_radius, draw_radius),
                draw_radius,
            )

            surface.blit(
                trail_surface,
                (
                    int(segment["x"] - draw_radius),
                    int(segment["y"] - draw_radius),
                ),
            )
