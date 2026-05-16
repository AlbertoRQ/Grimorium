"""Item visual que el jugador podra recoger mas adelante."""

import pygame
from game.entities.items.item_data import ITEM_DEFINITIONS 


class PickupItem:
    def __init__(self, x, y, item_id):
        self.x = x
        self.y = y
        self.item_id = item_id

        self.radius = 12
        
        data = ITEM_DEFINITIONS[item_id]
        self.name = data["name"]
        self.color = data["color"]


    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


    