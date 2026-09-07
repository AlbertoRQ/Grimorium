"""Small pixel shadows that sit on the ground beneath flying enemies."""

from functools import lru_cache

import pygame


@lru_cache(maxsize=32)
def flying_shadow(width):
    grid_width = max(5, round(width / 2))
    grid_height = max(3, round(grid_width * 0.3))
    shadow = pygame.Surface((grid_width, grid_height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (12, 12, 22, 65), shadow.get_rect())
    pygame.draw.ellipse(shadow, (10, 10, 18, 115),
                        (1, 1, grid_width - 2, max(1, grid_height - 2)))
    return pygame.transform.scale(shadow, (grid_width * 2, grid_height * 2))
