"""Pixel poison clouds and incandescent lava rain."""

import math
from functools import lru_cache

import pygame


@lru_cache(maxsize=96)
def cloud_sprite(width, height, ignited, frame):
    grid_w, grid_h = max(3, math.ceil(width / 2)), max(3, math.ceil(height / 2))
    cloud = pygame.Surface((grid_w, grid_h), pygame.SRCALPHA)
    # Overlapping round volumes share a single silhouette and a simple palette.
    lobes = ((.15, .62, .14, .25), (.31, .46, .21, .36),
             (.52, .39, .24, .37), (.73, .50, .20, .32),
             (.87, .64, .12, .23), (.50, .68, .37, .25))
    phase = (frame % 24) * math.tau / 24
    lobes = tuple((cx + math.sin(phase + index * 1.7) * .012,
                   cy + math.cos(phase + index * 1.3) * .025,
                   rx * (1 + math.sin(phase + index * 1.1) * .035),
                   ry * (1 + math.cos(phase + index * 1.5) * .04))
                  for index, (cx, cy, rx, ry) in enumerate(lobes))
    palette = ((29, 28, 40), (44, 42, 57), (63, 59, 77)) if ignited else (
        (92, 47, 123), (127, 67, 161), (163, 96, 193))
    flashes = (0, .25, .8, .4, .12, 0, 0, 0, 0, .15, .6, .2,
               0, 0, 0, 0, .3, .75, .25, .08, 0, 0, 0, 0)
    flash_strength = flashes[frame % 24] if ignited else 0
    flash_x, flash_y = ((.34, .49), (.67, .46), (.50, .58))[(frame % 24) // 8]
    for y in range(grid_h):
        ny = (y + .5) / grid_h
        for x in range(grid_w):
            nx = (x + .5) / grid_w
            cx, cy, rx, ry = min(lobes, key=lambda lobe:
                ((nx-lobe[0])/lobe[2])**2 + ((ny-lobe[1])/lobe[3])**2)
            local_x, local_y = (nx - cx) / rx, (ny - cy) / ry
            distance = local_x**2 + local_y**2
            if distance > 1:
                continue
            volume = math.sqrt(max(0, 1 - distance))
            # Light follows each rounded lobe instead of horizontal height bands.
            light = volume * .65 - local_x * .25 - local_y * .42
            shade = 0 if light < .22 else 2 if light > .68 else 1
            color = palette[shade]
            if flash_strength:
                # Buried light illuminates the vapour, without a visible bolt.
                glow = math.exp(-((nx - flash_x) / .20)**2 - ((ny - flash_y) / .28)**2)
                glow *= flash_strength * volume ** 2 * .65
                color = tuple(round(base + (lit - base) * glow)
                              for base, lit in zip(color, (185, 109, 225)))
            cloud.set_at((x, y), (*color, 235 if ignited else 210))
    cloud = pygame.transform.scale(cloud, (width, height))
    return cloud



def draw_lava_rain_drop(surface, x, y, radius, time, progress=0):
    # Two-pixel streaks remain slender but readable against the floor.
    phase = time * 19 + x * .37
    shimmer = .5 + .5 * math.sin(phase)
    length = min(9, max(4, round(radius * 2)) + round(progress * 2 + shimmer))
    streak = pygame.Surface((6, length + 4), pygame.SRCALPHA)
    lean = round(math.sin(phase * .55))
    for row in range(length):
        amount = row / max(1, length - 1)
        column = 2 + round(lean * (1 - amount))
        color = (255, round(80 + amount * 104 + shimmer * 20), 38, round(65 + amount * 180))
        streak.set_at((column, row + 2), color)
        streak.set_at((column + 1, row + 2), (255, round(65 + amount * 80), 30, round(50 + amount * 155)))
    streak.set_at((2, length + 1), (255, round(205 + shimmer * 35), 105, 245))
    if shimmer > .8:
        streak.set_at((2 + lean, 0), (255, 125, 35, 105))
    # Only the tail sways; the bright falling tip remains at the actual drop position.
    surface.blit(streak, (round(x) - 2, round(y) - length - 1))
