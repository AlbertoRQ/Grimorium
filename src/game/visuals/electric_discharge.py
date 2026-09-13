"""Thin pixel lightning and a short, purely visual impact spark."""

import math
import random

import pygame


def draw_discharge(surface, start, end, time, seed, arc_height=0):
    start, end = pygame.Vector2(start), pygame.Vector2(end)
    direction = end - start
    length = direction.length()
    if length < 1:
        return
    frame = int(time / 0.045)
    rng = random.Random(seed + frame * 7919)
    normal = pygame.Vector2(-direction.y, direction.x).normalize()
    steps = max(2, min(12, math.ceil(length / 24)))
    amplitude = min(6, length * 0.085)
    if arc_height > 0:
        steps = max(4, steps)
        amplitude = min(1.2, length * 0.035)
    points = [start]
    side = rng.choice((-1, 1))
    for index in range(1, steps):
        fraction = index / steps
        offset = side * amplitude * rng.uniform(0.5, 1)
        point = start.lerp(end, fraction) + normal * offset
        point.y -= arc_height * 4 * fraction * (1 - fraction)
        points.append(point)
        side *= -1
    points.append(end)
    bolts = [(points, False)]
    if length > 30:
        branch_start = points[rng.randrange(1, len(points) - 1)]
        branch_end = branch_start + direction.normalize() * rng.uniform(5, 10) + normal * rng.choice((-1, 1)) * rng.uniform(4, 8)
        bolts.append(([branch_start, branch_start.lerp(branch_end, 0.5) + normal * 2, branch_end], True))

    all_points = [p for path, _ in bolts for p in path]
    left = math.floor(min(p.x for p in all_points)) - 5
    top = math.floor(min(p.y for p in all_points)) - 5
    width = math.ceil(max(p.x for p in all_points)) - left + 6
    height = math.ceil(max(p.y for p in all_points)) - top + 6
    layer = pygame.Surface((width, height), pygame.SRCALPHA)
    paths = [([(round(p.x - left), round(p.y - top)) for p in path], branch) for path, branch in bolts]
    pulse = (1.0, 0.82, 0.94)[frame % 3]
    for path, branch in paths:
        pygame.draw.lines(layer, (255, 201, 45, round(34 * pulse)), False, path, 3 if branch else 7)
    for path, branch in paths:
        if not branch:
            pygame.draw.lines(layer, (255, 225, 70, round(155 * pulse)), False, path, 3)
    for path, branch in paths:
        pygame.draw.lines(layer, (255, 253, 223, round((190 if branch else 250) * pulse)), False, path, 1)
    surface.blit(layer, (left, top))


class ElectricImpact:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.timer = 0
        self.duration = 0.14
        self.finished = False

    def update(self, dt, enemies):
        self.timer += dt
        self.finished = self.timer >= self.duration
        return []

    def draw(self, surface):
        if self.finished:
            return
        progress = self.timer / self.duration
        alpha = round(220 * (1 - progress))
        layer = pygame.Surface((28, 28), pygame.SRCALPHA)
        phase = self.x * 0.17 + self.y * 0.13
        for index in range(3):
            angle = phase + index * math.tau / 3
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            start = pygame.Vector2(14, 14) + direction * (2 + progress * 6)
            end = start + direction * (3 * (1 - progress) + 1)
            pygame.draw.line(layer, (255, 222, 75, alpha), start, end, 1)
        if progress < 0.4:
            pygame.draw.line(layer, (255, 254, 225, alpha), (12, 14), (16, 14), 1)
            pygame.draw.line(layer, (255, 254, 225, alpha), (14, 12), (14, 16), 1)
        surface.blit(layer, (round(self.x - 14), round(self.y - 14)))
