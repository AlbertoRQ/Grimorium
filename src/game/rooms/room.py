""""Convierte room_data en habitaciones de verdad'"""

import pygame

from game import config


class Room:
    def __init__(self, layout, room_type):
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

        self.offset_x = (config.SCREEN_WIDTH - self.room_width) // 2
        self.offset_y = (config.SCREEN_HEIGHT - self.room_height) // 2

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
                    self.add_wall(pygame.Rect(x, y - config.WALL_THICKNESS, config.ROOM_CELL_SIZE, config.WALL_THICKNESS))

                if not self.is_floor_tile(row_index + 1, col_index):
                    self.add_wall(pygame.Rect(x, y + config.ROOM_CELL_SIZE, config.ROOM_CELL_SIZE, config.WALL_THICKNESS))

                if not self.is_floor_tile(row_index, col_index - 1):
                    self.add_wall(pygame.Rect(x - config.WALL_THICKNESS, y, config.WALL_THICKNESS, config.ROOM_CELL_SIZE))

                if not self.is_floor_tile(row_index, col_index + 1):
                    self.add_wall(pygame.Rect(x + config.ROOM_CELL_SIZE, y, config.WALL_THICKNESS, config.ROOM_CELL_SIZE))


    def draw(self, surface):
        for floor in self.floors:
            pygame.draw.rect(surface, (45, 45, 55), floor)
        
        for obj in self.objects:
            pygame.draw.rect(surface, (120, 100, 60), obj)

        for void in self.voids:
            pygame.draw.rect(surface, (5, 5, 10), void)

        for wall in self.walls:
            pygame.draw.rect(surface, (90, 90, 100), wall)


    def add_blocker(self, rect):
        self.blocking_rects.append(rect)

    def add_wall(self, rect):
        self.walls.append(rect)
        self.add_blocker(rect)

    def get_blocking_rects(self, include_walls=True, include_objects=True, include_voids=False):
        rects = []

        if include_walls:
            rects.extend(self.walls)
        if include_objects:
            rects.extend(self.objects)
        if include_voids:
            rects.extend(self.voids)

        return rects
