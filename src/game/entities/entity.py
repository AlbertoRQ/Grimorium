"""Clases base para entidades circulares del juego."""

import pygame

from game.systems.collisions import circles_collide


class Entity:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def circle_collides_with_rect(self, rect):
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))

        distance_x = self.x - closest_x
        distance_y = self.y - closest_y

        return distance_x * distance_x + distance_y * distance_y < self.radius * self.radius

    def collides_with_rects(self, rects):
        for rect in rects:
            if self.circle_collides_with_rect(rect):
                return True

        return False

    def collides_with_circles(self, circles):
        for circle in circles:
            if circle is self:
                continue
            if circles_collide(self, circle):
                return True
        return False

    def move_by(self, move_x, move_y, blockers, entities):
        old_x = self.x
        self.x += move_x

        if self.collides_with_rects(blockers) or self.collides_with_circles(entities):
            self.x = old_x

        old_y = self.y
        self.y += move_y

        if self.collides_with_rects(blockers) or self.collides_with_circles(entities):
            self.y = old_y


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class LivingEntity(Entity):
    def __init__(self, x, y, radius, color, max_health):
        super().__init__(x, y, radius, color)
        self.max_health = max_health
        self.health = max_health

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_dead(self):
        return self.health <= 0
