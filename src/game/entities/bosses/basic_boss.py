"""Jefe basico."""

import pygame

from game import config
from game.entities.enemies.enemy import Enemy
from game.visuals.animated_visual import AnimatedVisual


class BasicBoss(Enemy):
    def __init__(self, level=1):
        health = int(config.BOSS_MAX_HEALTH * (1.15 ** (level - 1)))
        regen = config.BOSS_REGEN * (1.05 ** (level - 1))

        super().__init__(
            (config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2),
            200,
            health,
            config.BOSS_RADIUS,
            config.ENEMY_COLOR,
            config.BOSS_DAMAGE,
            100
        )

        self.body_damage = config.BOSS_BODY_DAMAGE
        self.regen = regen
        self.direction_x = 1

        self.visual = AnimatedVisual(
            image_folder="enemies/rat",
            image_name="rat_animated.png",
            frame_cols=4,
            frame_rows=4,
            scale_x=self.radius * 3,
            scale_y=self.radius * 3,
            use_alpha=True,
            initial_state="idle",
            initial_facing="down",
            animations={
                "idle_right": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                "walk_right": {"row": 0, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_left": {"row": 1, "frames": [0], "speed": 0.25, "loop": True},
                "walk_left": {"row": 1, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_down": {"row": 2, "frames": [0], "speed": 0.25, "loop": True},
                "walk_down": {"row": 2, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_up": {"row": 3, "frames": [0], "speed": 0.25, "loop": True},
                "walk_up": {"row": 3, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},
            },
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
        old_y = self.y

        move_x = self.direction_x * self.speed * dt
        move_y = 0
        
        self.move_by(move_x, 0, blockers, entities)

        if self.x == old_x:
            self.direction_x *= -1

        real_move_x = self.x - old_x
        real_move_y = self.y - old_y

        self.update_visual_from_movement(real_move_x, real_move_y)
        


    def update(self, player, dt, blockers, entities):
        super().update(player, dt, blockers, entities)


    def draw(self, surface):
        super().draw(surface)