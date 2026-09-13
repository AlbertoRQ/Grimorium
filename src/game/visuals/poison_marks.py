"""Poison stack skulls using the game's existing tooltip icon."""

from functools import lru_cache

import pygame

from game.visuals.effect_images import effect_image


@lru_cache(maxsize=2)
def poison_mark(large=False):
    return effect_image("02_calavera_huesos.png" if large else "01_calavera_pequena.png")


def draw_poison_mark(surface, x, y, large=False, pulse=0):
    mark = poison_mark(large)
    surface.blit(mark, mark.get_rect(center=(round(x), round(y))))
    if large and pulse > 0.12:
        color = (233, 169, 245)
        for side in (-1, 1):
            px, py = round(x + side * 12), round(y - 2)
            pygame.draw.line(surface, color, (px - 1, py), (px + 1, py))
            pygame.draw.line(surface, color, (px, py - 1), (px, py + 1))
