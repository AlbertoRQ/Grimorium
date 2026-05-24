"""Jefe basico."""

import pygame

from game import config
from game.entities.enemies.enemy import Enemy


class BasicBoss(Enemy):
    def __init__(self):
        super().__init__(
            (config.SCREEN_WIDTH / 2,config.SCREEN_WIDTH / 2),
            200,
            config.BOSS_MAX_HEALTH,
            config.BOSS_RADIUS,
            config.ENEMY_COLOR,
            config.BOSS_DAMAGE,
            100
            
        )

        self.body_damage = config.BOSS_BODY_DAMAGE
        self.regen = config.BOSS_REGEN
        self.direction_x = 1

    def draw_boss_health_bar(self, surface, font):
        bar_width = config.SCREEN_WIDTH - 80
        bar_height = 30

        x = 40
        y = config.SCREEN_HEIGHT - bar_height - 30

        health_ratio = self.health / self.max_health
        health_ratio = max(0, min(1, health_ratio))

        fill_width = int(bar_width * health_ratio)

        background_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill_width, bar_height)

        pygame.draw.rect(surface, (50, 50, 50), background_rect)
        pygame.draw.rect(surface, (200, 30, 30), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), background_rect, 2)

        text = font.render(
            f"{self.health:.1f} / {self.max_health}",
            True,
            (255, 255, 255),
        )

        text_rect = text.get_rect(center=background_rect.center)
        surface.blit(text, text_rect)

    def move(self, player, dt, blockers, entities):
        old_x = self.x

        move_x = self.direction_x * self.speed * dt
        self.move_by(move_x, 0, blockers, entities)

        if self.x == old_x:
            self.direction_x *= -1


    def update(self, player, dt, blockers, entities):
        super().update(player, dt, blockers, entities)
