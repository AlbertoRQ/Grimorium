"""Three translucent pixel ice formations surrounding frozen enemies."""

from functools import lru_cache
from itertools import cycle

import pygame


ICE_DESIGNS = cycle(range(3))


@lru_cache(maxsize=48)
def ice_block_surfaces(body_width, body_height, variant=0):
    pixel_size = 2
    width = max(12, (body_width + 13) // pixel_size)
    height = max(18, (body_height + 25) // pixel_size)
    back = pygame.Surface((width, height), pygame.SRCALPHA)
    front = pygame.Surface((width, height), pygame.SRCALPHA)
    # One central spire, twin uneven spires, and a leaning tall spire with a spur.
    crowns = (
        [(0.04, 0.52), (0.20, 0.29), (0.48, 0.02), (0.72, 0.29), (0.96, 0.50)],
        [(0.04, 0.52), (0.24, 0.02), (0.49, 0.30), (0.74, 0.10), (0.96, 0.48)],
        [(0.04, 0.53), (0.17, 0.22), (0.39, 0.37), (0.67, 0.02), (0.96, 0.49)],
    )
    crown = [(round(x * (width - 1)), round(y * (height - 1)))
             for x, y in crowns[variant % 3]]
    bottom = height - 2
    outline = crown + [(width - 2, bottom - 2), (width - 5, bottom),
                       (4, bottom), (1, bottom - 3)]
    pygame.draw.polygon(back, (80, 160, 215, 85), outline)
    pygame.draw.polygon(front, (116, 203, 244, 48), outline)
    tips = [2] if variant % 3 == 0 else [1, 3]
    lines = []
    for index in tips:
        tip = crown[index]
        left = crown[index - 1]
        right = crown[index + 1]
        foot = (max(4, min(width - 5, tip[0] - 2)), bottom - 1)
        pygame.draw.polygon(back, (172, 229, 249, 110), [left, tip, right])
        pygame.draw.polygon(front, (216, 247, 255, 55), [left, tip, foot, (left[0], bottom - 3)])
        pygame.draw.polygon(front, (60, 144, 210, 75), [tip, right, (right[0], bottom - 3), foot])
        lines.append(((190, 237, 255, 100), tip, foot))
        lines.append(((225, 250, 255, 205), left, tip))
    lines.append(((220, 249, 255, 170), (4, bottom - 6), (5, bottom - 9)))
    lines.append(((193, 239, 255, 145),
                  (width - 7, bottom - 3), (width - 5, bottom - 5)))
    size = (width * pixel_size, height * pixel_size)
    back = pygame.transform.scale(back, size)
    front = pygame.transform.scale(front, size)
    # Draw strokes after scaling the facets so their width stays one screen pixel.
    def scaled(point):
        return (point[0] * pixel_size, point[1] * pixel_size)

    pygame.draw.polygon(front, (180, 237, 255, 165), [scaled(p) for p in outline], 1)
    for color, start, end in lines:
        pygame.draw.line(front, color, scaled(start), scaled(end), 1)
    return back, front
