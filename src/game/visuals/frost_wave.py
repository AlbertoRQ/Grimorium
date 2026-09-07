"""Pixel frost mist and drifting ice flecks for an expanding cold wave."""

import math

import pygame


def draw_frost_wave(surface, x, y, radius, progress):
    if radius <= 0 or progress >= 1:
        return
    fade = (1 - progress) ** 0.65
    size = math.ceil(radius * 2) + 20
    grid_size = max(4, math.ceil(size / 2))
    mist = pygame.Surface((grid_size, grid_size), pygame.SRCALPHA)
    center = grid_size / 2
    outer_radius = radius / 2
    thickness = min(outer_radius * 0.65, 3 + radius * 0.05)
    phase = x * 0.013 + y * 0.017

    def point(angle, distance):
        return (round(center + math.cos(angle) * distance),
                round(center + math.sin(angle) * distance))

    # Uneven, overlapping density bands form a cold front, without a hard rim.
    for spread, opacity in ((1.5, 22), (1.0, 40), (0.5, 64)):
        count = max(48, min(120, round(radius * 1.5)))
        for index in range(count):
            angle = index * math.tau / count
            next_angle = (index + 1) * math.tau / count
            points = []
            for a, inner in ((angle, False), (next_angle, False),
                             (next_angle, True), (angle, True)):
                ripple = math.sin(a * 7 + phase) * 0.65 + math.sin(a * 13 - phase) * 0.35
                edge = outer_radius - thickness * 0.25 + ripple * thickness * 0.18
                distance = max(0, edge - thickness * spread if inner else edge + spread * 0.4)
                points.append(point(a, distance))
            density = 0.8 + 0.2 * math.sin(angle * 5 + phase + progress * 3)
            pygame.draw.polygon(mist, (164, 223, 241, round(opacity * fade * density)), points)

    # Broken streaks and a few tiny crystals travel with the front.
    detail = pygame.Surface((grid_size * 2, grid_size * 2), pygame.SRCALPHA)
    for index in range(18):
        angle = index * math.tau / 18 + phase + math.sin(index * 2.3) * 0.06
        distance = outer_radius - thickness * (0.2 + (index % 4) * 0.22)
        a, b, c = [point(angle + offset, max(0, distance)) for offset in (-0.035, 0, 0.035)]
        points = [(px * 2, py * 2) for px, py in (a, b, c)]
        pygame.draw.lines(detail, (216, 245, 255, round(125 * fade)), False, points, 1)
        if index % 3 == 0 and radius > 16:
            px, py = point(angle + 0.08, outer_radius + 1 + math.sin(index) * 1.5)
            px, py = px * 2, py * 2
            color = (231, 250, 255, round(160 * fade))
            pygame.draw.line(detail, color, (px - 2, py), (px + 2, py))
            pygame.draw.line(detail, color, (px, py - 2), (px, py + 2))
    position = (round(x - grid_size), round(y - grid_size))
    surface.blit(pygame.transform.scale(mist, detail.get_size()), position)
    surface.blit(detail, position)
