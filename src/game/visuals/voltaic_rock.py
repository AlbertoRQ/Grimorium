"""Pixel basalt shards with hot fissures and a brief fragmentation burst."""

import math
import random

import pygame

from game.visuals.effect_images import effect_image, effect_frame


def draw_voltaic_rock(surface, x, y, radius, heat, time, angle=0, energized=True):
    radius = max(3, radius)
    heat = max(0, min(1, heat))
    size = math.ceil(radius * 3) + 20
    layer = pygame.Surface((size, size), pygame.SRCALPHA)
    center = pygame.Vector2(size // 2, size // 2)

    def point(px, py):
        p = pygame.Vector2(px, py).rotate(angle) * radius + center
        return round(p.x), round(p.y)

    def rock_point(px, py):
        return point(px * 0.65, py * 0.65)

    shape = [(-1.1, -0.25), (-0.38, -0.50), (-0.20, -1.05),
             (0.18, -0.45), (0.73, -0.70), (0.48, -0.08),
             (0.96, 0.28), (0.32, 0.42), (0.10, 0.94),
             (-0.27, 0.50), (-0.82, 0.63), (-0.56, 0.05)]
    if energized:
        image = effect_frame("14_roca_lava.png", min(2, int(heat * 3)))
        scale = radius / 8
    else:
        image = effect_image("15_piedra_brasa.png")
        scale = radius / 4
    image = pygame.transform.scale(image, (max(1, round(image.get_width() * scale)),
                                           max(1, round(image.get_height() * scale))))
    image = pygame.transform.rotate(image, -angle)
    layer.blit(image, image.get_rect(center=(round(center.x), round(center.y))))
    if not energized:
        surface.blit(layer, (round(x - center.x), round(y - center.y)))
        return
    # Short irregular loops leave the crust and reconnect at another fissure.
    rng = random.Random(int(time / 0.055) * 7919 + int(angle * 13))
    arcs = []
    arc_count = int(heat > 0.55 and int(time / 0.07) % 4 == 0)
    for index in range(arc_count):
        start_index = (rng.randrange(len(shape)) + index * 4) % len(shape)
        end_index = (start_index + rng.choice((2, 3, 4))) % len(shape)
        start = pygame.Vector2(rock_point(*shape[start_index]))
        end = pygame.Vector2(rock_point(*shape[end_index]))
        outward = (start + end) / 2 - center
        if outward.length_squared() < 0.1:
            outward = pygame.Vector2(0, -1)
        outward = outward.normalize()
        tangent = pygame.Vector2(-outward.y, outward.x)
        reach = rng.uniform(1, 2) + radius * 0.20
        arc = [start]
        for step in range(1, 5):
            fraction = step / 5
            arc.append(start.lerp(end, fraction)
                       + outward * math.sin(fraction * math.pi) * reach
                       + tangent * rng.uniform(-1.5, 1.5))
        arc.append(end)
        arcs.append([(round(p.x), round(p.y)) for p in arc])
    glow = pygame.Surface(layer.get_size(), pygame.SRCALPHA)
    for arc in arcs:
        pygame.draw.lines(glow, (255, 206, 65, 45), False, arc, 3)
    layer.blit(glow, (0, 0))
    for arc in arcs:
        pygame.draw.lines(layer, (255, 239, 159, 165), False, arc, 1)
    surface.blit(layer, (round(x - center.x), round(y - center.y)))


class VoltaicRockBurst:
    def __init__(self, x, y, direction, small=False):
        self.x, self.y = x, y
        self.angle = math.atan2(direction.y, direction.x)
        self.small = small
        self.timer = 0
        self.finished = False

    def update(self, dt, enemies):
        self.timer += dt
        self.finished = self.timer >= 0.20
        return []

    def draw(self, surface):
        if self.finished:
            return
        progress = self.timer / 0.20
        layer = pygame.Surface((64, 64), pygame.SRCALPHA)
        for index in range(5):
            angle = self.angle + (index - 2) * 0.55
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            start = pygame.Vector2(32, 32) + direction * (3 + progress * (12 if self.small else 22))
            draw_voltaic_rock(layer, start.x, start.y, 3, 0, self.timer,
                              angle=index * 71 + progress * 100, energized=False)
        layer.set_alpha(round(255 * (1 - progress)))
        surface.blit(layer, (round(self.x - 32), round(self.y - 32)))
