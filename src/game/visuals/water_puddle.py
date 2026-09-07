"""Shallow pixel water with an uneven shore and broken moving reflections."""

import math

import pygame


def draw_water(surface, time, phase):
    width, height = surface.get_size()
    center_x, center_y = (width - 1) / 2, (height - 1) / 2
    shore = []
    for index in range(40):
        angle = index * math.tau / 40
        reach = (0.91 + 0.045 * math.sin(angle * 3 + phase)
                 + 0.035 * math.sin(angle * 7 - phase))
        shore.append((round(center_x + math.cos(angle) * center_x * reach),
                      round(center_y + math.sin(angle) * center_y * reach)))
    pygame.draw.polygon(surface, (78, 171, 205, 68), shore)

    # Broad patches suggest depth without tracing a rim around the water.
    # patches = (
    #     ((125, 204, 226, 78), [(0.16, 0.40), (0.32, 0.24), (0.64, 0.28),
    #                           (0.78, 0.42), (0.56, 0.49), (0.30, 0.47)]),
    #     ((99, 186, 214, 78), [(0.22, 0.63), (0.48, 0.53), (0.81, 0.57),
    #                          (0.70, 0.72), (0.43, 0.79), (0.27, 0.71)]),
    # )
    # for color, points in patches:
    #     pygame.draw.polygon(surface, color,
    #                         [(round(x * (width - 1)), round(y * (height - 1))) for x, y in points])

    if width < 10 or height < 6:
        return
    # Short horizontal glints shimmer slowly; no closed circular outlines.
    # for index, (x, y, length) in enumerate(((0.23, 0.35, 0.22), (0.56, 0.59, 0.18), (0.34, 0.74, 0.12))):
    #     wave = math.sin(time * 1.8 + phase + index * 2.1)
    #     start_x = round(width * x + wave)
    #     start_y = round(height * y + wave * 0.6)
    #     end_x = min(width - 2, start_x + max(2, round(width * length)))
    #     alpha = round(95 + 25 * wave)
    #     pygame.draw.lines(surface, (192, 235, 244, alpha), False,
    #                       [(start_x, start_y), (start_x + 1, start_y + 1),
    #                        (end_x - 1, start_y + 1), (end_x, start_y)], 1)
