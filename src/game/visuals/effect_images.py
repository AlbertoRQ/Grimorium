"""Cached artist-authored effect images; shared surfaces must not be mutated."""

from functools import lru_cache

import pygame

from game.utils.paths import asset_path


@lru_cache(maxsize=32)
def effect_image(filename):
    return pygame.image.load(asset_path("images", "effects", filename))


@lru_cache(maxsize=16)
def effect_frame(filename, frame):
    # Explicit cells keep animation stable even when the artist changes pixels.
    cells = {
        "05_llamas.png": ((0, 0, 5, 7), (11, 0, 5, 7),
                          (22, 0, 5, 7), (33, 0, 5, 7)),
        "14_roca_lava.png": ((0, 0, 11, 14), (17, 0, 14, 14),
                             (37, 0, 14, 14)),
    }
    rects = cells[filename]
    return effect_image(filename).subsurface(rects[frame % len(rects)]).copy()
