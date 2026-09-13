"""Three authored ice formations fitted to the enemy's visible body."""

from functools import lru_cache
from itertools import cycle

import pygame

from game.visuals.effect_images import effect_image


ICE_DESIGNS = cycle(range(3))


@lru_cache(maxsize=48)
def ice_block_surfaces(body_width, body_height, variant=0):
    size = (max(12, (body_width + 13) // 2) * 2,
            max(18, (body_height + 25) // 2) * 2)
    image = effect_image(("06_hielo_1.png", "07_hielo_2.png", "08_hielo_3.png")[variant % 3])
    # The PNG contains both translucent planes; overlay it once to retain its alpha.
    front = pygame.Surface(size, pygame.SRCALPHA)
    target = (max(1, size[0] - 5), max(1, size[1] - (6 if variant % 3 == 1 else 5)))
    image = pygame.transform.scale(image, target)
    front.blit(image, image.get_rect(midbottom=(size[0] // 2, size[1] - 2)))
    return pygame.Surface(size, pygame.SRCALPHA), front
