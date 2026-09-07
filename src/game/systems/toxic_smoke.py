"""Shared soft lilac smoke for the toxic trail and overload field."""

import math
import random
from functools import lru_cache

import pygame

SMOKE_COLOR = (185, 112, 218)
SMOKE_ALPHA = 125
SMOKE_PIXEL_SIZE = 3


@lru_cache(maxsize=32)
def smoke_sprite(size, variant):
    """Return a cached density sprite; callers must copy before modifying it."""
    grid_size = max(4, math.ceil(size / SMOKE_PIXEL_SIZE))
    sprite = pygame.Surface((grid_size, grid_size), pygame.SRCALPHA)
    phase = variant * 1.73
    rng = random.Random(7301 + variant)
    clouds = [
        (rng.uniform(-0.65, 0.65), rng.uniform(-0.65, 0.65),
         rng.uniform(0.28, 0.55), rng.uniform(0.12, 0.22))
        for _ in range(5)
    ]
    for y in range(grid_size):
        ny = (y + 0.5) / grid_size * 2 - 1
        for x in range(grid_size):
            nx = (x + 0.5) / grid_size * 2 - 1
            # Broad soft clouds avoid the thin ridges of periodic noise.
            warp_x = nx + 0.12 * math.sin(ny * 5 + phase)
            warp_y = ny + 0.10 * math.sin(nx * 6 - phase)
            distance = math.hypot(warp_x, warp_y)
            envelope = max(0, 1 - distance * distance) ** 2
            boundary = max(0, 1 - max(abs(nx), abs(ny)) ** 6) ** 2
            cloud = 0.55 + 0.55 * sum(
                strength * math.exp(-((nx - cx) ** 2 + (ny - cy) ** 2) / (2 * spread ** 2))
                for cx, cy, spread, strength in clouds
            )
            alpha = int(SMOKE_ALPHA * envelope * boundary * cloud)
            # Smaller opacity steps soften tonal jumps without smoothing pixels.
            alpha = (alpha // 6) * 6
            sprite.set_at((x, y), (*SMOKE_COLOR, alpha))
    return pygame.transform.scale(sprite, (size, size))
