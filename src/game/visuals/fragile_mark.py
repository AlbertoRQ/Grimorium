"""Cracked pixel crystals and sparse frost flecks for Fragile Mark."""

import math

import pygame

from game.visuals.effect_images import effect_image


def draw_fragile_crystal(surface, x, y, sentenced=False, pulse=0, time=0):
    image = effect_image("04_cristal_plus.png" if sentenced else "03_cristal_fragil.png")
    if sentenced:
        image = image.copy()
        brightness = .85 + .15 * math.sin(time * 5)
        image.set_alpha(round(min(255, 225 + 30 * brightness + 20 * min(1, pulse / .28))))
    surface.blit(image, image.get_rect(center=(round(x), round(y))))


def draw_fragile_flecks(surface, x, y, radius, time, sentenced=False):
    size = max(16, math.ceil(radius * 3 + 12))
    layer = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    for index in range(3):
        progress = (time * .65 + index / 3) % 1
        side = -1 if index % 2 else 1
        px = round(center + side * radius * (.55 + progress * .30)
                   + math.sin(time * 2 + index) * 1.5)
        py = round(center - radius * .55 + progress * radius * .85)
        alpha = round(155 * math.sin(progress * math.pi))
        color = (201, 156, 231, alpha) if sentenced else (183, 224, 245, alpha)
        pygame.draw.line(layer, color, (px, py), (px + 1, py + 1), 1)
        if index == 1:
            layer.set_at((px + 1, py), color)
    surface.blit(layer, (round(x) - center, round(y) - center))
