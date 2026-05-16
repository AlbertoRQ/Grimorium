"""Funciones pequeñas que usaras en varios sitios."""

import pygame


def clamp(value, minimum, maximum):
    """Limita un valor entre un minimo y un maximo."""
    return max(minimum, min(maximum, value))


def distance(point_a, point_b):
    """Distancia entre dos puntos."""
    return pygame.Vector2(point_a).distance_to(point_b)


def normalize_vector(vector):
    """Devuelve el vector normalizado o un vector vacio si no hay direccion."""
    vector = pygame.Vector2(vector)

    if vector.length_squared() == 0:
        return pygame.Vector2()

    return vector.normalize()
