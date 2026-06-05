"""Clases base para entidades circulares del juego."""

import pygame

from game.systems.collisions import circles_collide
from game.utils.paths import asset_path


class Entity:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.sprite_sheet = None
        self.sprite = None
        self.frame_cols = 1
        self.frame_rows = 1
        self.frame_width = 0
        self.frame_height = 0
        self.sprite_size_x = self.radius * 3
        self.sprite_size_y = self.radius * 3

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
        if self.sprite is None:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            return

        sprite_rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.sprite, sprite_rect)

class LivingEntity(Entity):
    def __init__(self, x, y, radius, color, base_color, max_health):
        super().__init__(x, y, radius, color)
        self.max_health = max_health
        self.health = max_health
        self.base_color = color
        

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_dead(self):
        return self.health <= 0
    

    def setup_sprite(self, image_folder, image_name, frame_cols=1, frame_rows=1, colorkey=None, scale=3):
        self.sprite_sheet = pygame.image.load(
            asset_path("images", image_folder, image_name)
        ).convert()

        if colorkey is not None:
            self.sprite_sheet.set_colorkey(colorkey)

        self.frame_cols = frame_cols
        self.frame_rows = frame_rows

        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()

        self.frame_width = sheet_width // self.frame_cols
        self.frame_height = sheet_height // self.frame_rows

        self.sprite_size_x = self.radius * scale
        self.sprite_size_y = self.radius * scale

        self.set_sprite_frame(0, 0)


    def get_frame(self, col, row):
        frame_rect = pygame.Rect(
            col * self.frame_width,
            row * self.frame_height,
            self.frame_width,
            self.frame_height,
        )
        return self.sprite_sheet.subsurface(frame_rect).copy()


    def set_sprite_frame(self, col, row):
        self.sprite = self.get_frame(col, row)
        self.sprite = pygame.transform.scale(
            self.sprite,
            (self.sprite_size_x, self.sprite_size_y),
        )
