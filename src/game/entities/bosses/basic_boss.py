"""Jefe basico."""

import pygame

from game import config
from game.entities.enemies.enemy import Enemy


class BasicBoss(Enemy):
    def __init__(self):
        super().__init__(
            (config.SCREEN_WIDTH / 2,config.SCREEN_HEIGHT / 2),
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

        self.setup_sprite(
            image_folder="enemies",
            image_name="rat.bmp",
            frame_cols=4,
            frame_rows=1,
            colorkey=(84, 206, 76),
            scale=3,
        )

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

        if self.direction_x > 0:
            self.set_sprite_frame(1, 0)
        else:
            self.set_sprite_frame(0, 0)

        if self.x == old_x:
            self.direction_x *= -1

    def update(self, player, dt, blockers, entities):
        super().update(player, dt, blockers, entities)


    def draw(self, surface):
        if self.sprite is None:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            return

        sprite_to_draw = self.sprite
        base_color = getattr(self, "base_color", self.color)

        if self.color != base_color:
            mask = pygame.mask.from_surface(self.sprite)
            color_overlay = mask.to_surface(
                setcolor=(*self.color, 120),
                unsetcolor=(0, 0, 0, 0),
            ).convert_alpha()

            sprite_to_draw = self.sprite.copy()
            sprite_to_draw.blit(color_overlay, (0, 0))

        if getattr(self, "damage_flash_timer", 0) > 0:
            mask = pygame.mask.from_surface(sprite_to_draw)
            damage_overlay = mask.to_surface(
                setcolor=(120, 0, 0, 180),
                unsetcolor=(0, 0, 0, 0),
            ).convert_alpha()

            sprite_to_draw = sprite_to_draw.copy()
            sprite_to_draw.blit(damage_overlay, (0, 0))

        sprite_rect = sprite_to_draw.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(sprite_to_draw, sprite_rect)