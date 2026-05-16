"""Boton basico reutilizable para menus."""

import pygame

from game import config


class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, 42)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        color = config.BUTTON_HOVER_COLOR if hovered else config.BUTTON_COLOR

        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, config.HUD_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
