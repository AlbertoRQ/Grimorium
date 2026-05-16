"""Trigger visual."""

import pygame

from game import config

from game.entities.items.item_data import ITEM_DEFINITIONS 


class Trigger:
    def __init__(self, rect):
        self.rect = rect
        self.color = (80, 140, 200)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


    