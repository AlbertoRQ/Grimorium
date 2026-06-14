""""Convierte room_data en habitaciones de verdad'"""

import pygame

from game import config
from game.utils.paths import asset_path


class Room:
    def __init__(self, layout, room_type, viewport_width, viewport_height):
        self.layout = layout
        self.room_type = room_type
        self.cleared = False

        self.walls = []
        self.objects = []
        self.voids = []
        self.floors = []
        self.blocking_rects = []

        self.player_spawn = None
        self.boss_spawn = None
        self.enemy_spawns = []
        self.item_spawns = []
        self.trigger_spawns = []

        self.room_width = max(len(row) for row in self.layout) * config.ROOM_CELL_SIZE
        self.room_height = len(self.layout) * config.ROOM_CELL_SIZE

        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.room_width = max(len(row) for row in self.layout) * config.ROOM_CELL_SIZE
        self.room_height = len(self.layout) * config.ROOM_CELL_SIZE

        self.offset_x = (self.viewport_width - self.room_width) // 2
        self.offset_y = (self.viewport_height - self.room_height) // 2
       

        wall_top = pygame.image.load(
            asset_path("images", "tiles", "wall_top.png")
        ).convert_alpha()

        wall_top = pygame.transform.scale(
            wall_top,
            (config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE)
        )

        self.wall_sprites = {
            "top": wall_top,
            "bottom": pygame.transform.rotate(wall_top, 180),
            "left": pygame.transform.rotate(wall_top, 90),
            "right": pygame.transform.rotate(wall_top, -90),
        }

        self.corners = []
        self.corner_keys = set()

        outer_top_right = pygame.image.load(
            asset_path("images", "tiles", "outer_top_right.png")
        ).convert_alpha()
        outer_top_right = pygame.transform.scale(
            outer_top_right,
            (config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE)
        )

        inner_bottom_right = pygame.image.load(
            asset_path("images", "tiles", "inner_bottom_right.png")
        ).convert_alpha()
        inner_bottom_right = pygame.transform.scale(
            inner_bottom_right,
            (config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE)
        )

        self.corner_sprites = {
            "outer_top_right": outer_top_right,
            "outer_top_left": pygame.transform.flip(outer_top_right, True, False),
            "outer_bottom_right": pygame.transform.flip(outer_top_right, False, True),
            "outer_bottom_left": pygame.transform.flip(outer_top_right, True, True),

            "inner_bottom_right": inner_bottom_right,
            "inner_bottom_left": pygame.transform.flip(inner_bottom_right, True, False),
            "inner_top_right": pygame.transform.flip(inner_bottom_right, False, True),
            "inner_top_left": pygame.transform.flip(inner_bottom_right, True, True),
        }

        self.load_layout()

    def is_floor_tile(self, row, col):
        if row < 0 or row >= len(self.layout):
            return False

        if col < 0 or col >= len(self.layout[row]):
            return False

        tile = self.layout[row][col]

        return tile in [".", "P", "B", "E", "O", "N", "V", "I"]

    def load_layout(self):
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                x = self.offset_x + col_index * config.ROOM_CELL_SIZE 
                y = self.offset_y + row_index * config.ROOM_CELL_SIZE 

                rect = pygame.Rect(x, y, config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE )

                if not self.is_floor_tile(row_index, col_index):
                    continue

                self.floors.append(rect)

                self.detect_corners_for_tile(row_index, col_index, x, y)

                tile = self.layout[row_index][col_index]

                if tile == "P":
                    self.player_spawn = (x + config.ROOM_CELL_SIZE //2, y + config.ROOM_CELL_SIZE //2)

                elif tile == "B":
                    self.boss_spawn = (x + config.ROOM_CELL_SIZE //2, y + config.ROOM_CELL_SIZE//2)

                elif tile == "E":
                    enemy = (x + config.ROOM_CELL_SIZE //2, y + config.ROOM_CELL_SIZE //2)
                    self.enemy_spawns.append(enemy)

                elif tile == "O":
                    self.objects.append(rect)
                    self.add_blocker(rect)

                elif tile == "V":
                    self.voids.append(rect)

                elif tile == "N":
                    self.trigger_spawns.append(rect)

                elif tile == "I":
                    item = (
                        x + config.ROOM_CELL_SIZE // 2,
                        y + config.ROOM_CELL_SIZE // 2,
                    )
                    self.item_spawns.append(item)

                        
                if not self.is_floor_tile(row_index - 1, col_index):
                    self.add_wall(pygame.Rect(x, y - config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE),
                                  "top")

                if not self.is_floor_tile(row_index + 1, col_index):
                    self.add_wall(pygame.Rect(x, y + config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE),
                                  "bottom")

                if not self.is_floor_tile(row_index, col_index - 1):
                    self.add_wall(pygame.Rect(x - config.ROOM_CELL_SIZE, y, config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE),
                                  "left")

                if not self.is_floor_tile(row_index, col_index + 1):
                    self.add_wall(pygame.Rect(x + config.ROOM_CELL_SIZE, y, config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE),
                                  "right")


    def add_blocker(self, rect):
        self.blocking_rects.append(rect)


    def add_wall(self, rect, side):
        self.walls.append({
            "rect": rect,
            "side": side,
        })
        self.add_blocker(rect)

    
    def add_corner(self, x, y, corner_type):
        key = (x, y, corner_type)

        if key in self.corner_keys:
            return

        self.corner_keys.add(key)
        self.corners.append({
            "x": x,
            "y": y,
            "type": corner_type,
        })

    
    def detect_corners_for_tile(self, row, col, x, y):
        tile_size = config.ROOM_CELL_SIZE

        up = self.is_floor_tile(row - 1, col)
        down = self.is_floor_tile(row + 1, col)
        left = self.is_floor_tile(row, col - 1)
        right = self.is_floor_tile(row, col + 1)

        up_left = self.is_floor_tile(row - 1, col - 1)
        up_right = self.is_floor_tile(row - 1, col + 1)
        down_left = self.is_floor_tile(row + 1, col - 1)
        down_right = self.is_floor_tile(row + 1, col + 1)

        if not up and not left:
            self.add_corner(x - tile_size, y - tile_size, "outer_top_left")

        if not up and not right:
            self.add_corner(x + tile_size, y - tile_size, "outer_top_right")

        if not down and not left:
            self.add_corner(x - tile_size, y + tile_size, "outer_bottom_left")

        if not down and not right:
            self.add_corner(x + tile_size, y + tile_size, "outer_bottom_right")

        if up and left and not up_left:
            self.add_corner(x - tile_size, y - tile_size, "inner_bottom_right")

        if up and right and not up_right:
            self.add_corner(x + tile_size, y - tile_size, "inner_bottom_left")

        if down and left and not down_left:
            self.add_corner(x - tile_size, y + tile_size, "inner_top_right")

        if down and right and not down_right:
            self.add_corner(x + tile_size, y + tile_size, "inner_top_left")


    def get_blocking_rects(self, include_walls=True, include_objects=True, include_voids=False):
        rects = []

        if include_walls:
            rects.extend(wall["rect"] for wall in self.walls)
        if include_objects:
            rects.extend(self.objects)
        if include_voids:
            rects.extend(self.voids)

        return rects


    def draw(self, surface):
        for floor in self.floors:
            pygame.draw.rect(surface, (45, 45, 55), floor)
        
        for obj in self.objects:
            pygame.draw.rect(surface, (120, 100, 60), obj)

        for void in self.voids:
            pygame.draw.rect(surface, (5, 5, 10), void)

        for wall in self.walls:
            sprite = self.wall_sprites[wall["side"]]
            surface.blit(sprite, wall["rect"].topleft)


        for corner in self.corners:
            sprite = self.corner_sprites[corner["type"]]
            surface.blit(sprite, (corner["x"], corner["y"]))
