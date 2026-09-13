"""Authored water silhouette scaled to the existing visual footprint."""

import pygame

from game.visuals.effect_images import effect_image


def draw_water(surface, time, phase):
    width, height = surface.get_size()
    if width <= 0 or height <= 0:
        return
    image = effect_image("10_charco.png")
    # Preserve the transparent margin of the original 68 by 40 reference.
    image = pygame.transform.scale(image, (max(1, round(width * 63 / 68)),
                                            max(1, round(height * 37 / 40))))
    surface.blit(image, image.get_rect(center=surface.get_rect().center))
