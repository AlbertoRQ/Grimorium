"""Small animated pixel flames for burning enemies."""

import math
from functools import lru_cache

import pygame

from game.visuals.effect_images import effect_frame


@lru_cache(maxsize=12)
def flame_sprite(frame, pixel_size):
    sprite = effect_frame("05_llamas.png", frame)
    return pygame.transform.scale(sprite, (sprite.get_width() * pixel_size,
                                           sprite.get_height() * pixel_size))


def draw_burn_flames(surface, body_rect, time, phase, stacks):
    pixel_size = max(1, min(2, body_rect.height // 48))
    count = 2 + int(stacks >= 3)
    for index in range(count):
        progress = (time * 1.25 + index / count + phase) % 1
        frame = (int(time * 10) + index) % 4
        flame = flame_sprite(frame, pixel_size).copy()
        fade = min(1, progress / 0.15, (1 - progress) / 0.4)
        flame.set_alpha(round(210 * fade))
        # Small staggered wisps rise from the body and fade out gently.
        side = ((index * 0.618) % 1 - 0.5) * body_rect.width * 0.85
        sway = math.sin(time * 6 + index * 2.4) * pixel_size
        x = round(body_rect.centerx + side + sway)
        y = round(body_rect.centery + body_rect.height * (0.30 - progress * 0.65))
        surface.blit(flame, flame.get_rect(midbottom=(x, y)))
