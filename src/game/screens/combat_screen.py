import pygame

from game import config
from game.rooms.room import Room
from game.screens.base_screen import BaseScreen
from game.systems.collisions import (
    resolve_player_bullets_vs_enemies,
    resolve_enemy_bullets_vs_player,
    resolve_enemies_touch_player,
    circles_collide
)
from game.entities.items.pickup_item import PickupItem
from game.entities.items.item_data import choose_random_item_id

from game.entities.triggers.trigger import Trigger


WEAPON_KEYS = {
    pygame.K_1: "normal",
    pygame.K_2: "gatling",
    pygame.K_3: "spread",
}


class CombatScreen(BaseScreen):
    def __init__(self, game, room_layout, room_type):
        super().__init__(game)

        self.player = self.game.player
        self.player.sprite_size_x = self.player.radius * 3
        self.player.sprite_size_y = self.player.radius * 3
        self.player.sprite = self.player.get_frame(2, 0)
        self.sprite = pygame.transform.scale(self.player.sprite, (self.player.sprite_size_x, self.player.sprite_size_y))
        self.bullets = []
        self.enemies = []
        self.enemies_bullets = []
        self.font = pygame.font.Font(None, 36)

        self.room = Room(room_layout, room_type)
        self.place_player_at_spawn()

        self.complete = False
        self.items = []
        self.items_spawned = False
        self.reward_item_count = 3

        self.triggers = []
        self.triggers_spawned = False

        self.room_time = 0

    def get_blockers(self):
        return self.room.get_blocking_rects()

    def place_player_at_spawn(self):
        if self.room.player_spawn is not None:
            self.player.x, self.player.y = self.room.player_spawn

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.go_to_menu()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            self.kill_all_enemies()
            return

        if event.type == pygame.KEYDOWN:
            self.handle_weapon_key(event.key)

    def go_to_menu(self):
        from game.screens.menu_screen import MenuScreen

        self.game.screen_manager.set_screen(MenuScreen(self.game))

    def handle_weapon_key(self, key):
        if key in WEAPON_KEYS:
            self.player.bullet_type = WEAPON_KEYS[key]

    def kill_all_enemies(self):
        self.enemies = []

    def update_player(self, dt):
        keys = pygame.key.get_pressed()
        self.player.move(keys, dt, self.get_blockers(), [])
        self.player.update(dt)

    def update_player_shooting(self):
        keys = pygame.key.get_pressed()
        self.bullets.extend(self.player.shoot(keys))

    def update_enemies(self, dt):
        for enemy in self.enemies:
            new_bullets = enemy.update(self.player, dt, self.get_blockers(), self.enemies)

            if new_bullets:
                self.enemies_bullets.extend(new_bullets)

    def update_projectiles(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)

        for enemy_bullet in self.enemies_bullets:
            enemy_bullet.update(dt)

        self.bullets = [
            bullet for bullet in self.bullets
            if not bullet.is_offscreen()
        ]

        self.enemies_bullets = [
            bullet for bullet in self.enemies_bullets
            if not bullet.is_offscreen()
        ]


    def resolve_collisions(self):
        self.bullets, self.enemies, coins_gained = resolve_player_bullets_vs_enemies(
            self.bullets,
            self.enemies,
            self.player.damage,
        )
        self.player.coins += coins_gained

        self.enemies_bullets = resolve_enemy_bullets_vs_player(
            self.enemies_bullets,
            self.player,
        )

        self.enemies, coins_gained = resolve_enemies_touch_player(
            self.enemies,
            self.player,
            self.get_blockers()
        )
        self.player.coins += coins_gained

    def draw(self, surface):
        surface.fill(config.BACKGROUND_COLOR)

        self.room.draw(surface)

        for item in self.items:
            item.draw(surface)

        for trigger in self.triggers:
            trigger.draw(surface)

        self.player.draw(surface)

        for bullet in self.bullets:
            bullet.draw(surface)

        for enemy in self.enemies:
            enemy.draw(surface)

        for enemy_bullet in self.enemies_bullets:
            enemy_bullet.draw(surface)

        lines = [f"Time: {self.room_time:.1f}"]
        x = 50
        y = 150
        line_height = 28
        for line in lines:
            text = self.font.render(line, True, config.HUD_COLOR)
            surface.blit(text, (x, y))
            y += line_height

        self.draw_extra(surface)
        self.draw_hud(surface)

    def draw_extra(self, surface):
        pass

    def draw_hud(self, surface):

        self.player.draw_player_stats(surface, self.font)
        self.player.draw_player_health(surface, self.font)
        self.player.draw_player_items(surface, self.font)

    def check_game_over(self):
        if self.player.health <= 0:
            from game.screens.game_over_screen import GameOverScreen

            self.game.screen_manager.set_screen(GameOverScreen(self.game))
    
    def is_complete(self):
        if self.complete:
            return

        if len(self.enemies) == 0:
            self.complete = True


    def spawn_reward_items(self):
        for item_pos in self.room.item_spawns:
            x, y = item_pos
            item_id = choose_random_item_id(self.player)
            self.items.append(PickupItem(x, y, item_id))
        
    def update_items(self):
        if not self.complete:
            return

        if not self.items_spawned:
            self.spawn_reward_items()
            self.items_spawned = True

        self.collect_items()


    def collect_items(self):
        items_left = []

        for item in self.items:
            if circles_collide(self.player, item):
                self.player.apply_item(item)
            else:
                items_left.append(item)

        self.items = items_left


    def spawn_triggers(self):
        for trigger_rect in self.room.trigger_spawns:
            self.triggers.append(Trigger(trigger_rect))

    def update_triggers(self):
        if not self.complete:
            return

        if not self.triggers_spawned:
            self.spawn_triggers()
            self.triggers_spawned = True

    def check_next_trigger(self):
        if not self.complete:
            return

        for trigger in self.triggers:
            if self.player.circle_collides_with_rect(trigger.rect):
                self.reward_end_of_room()
                self.game.finish_current_screen()
                return
            
    def reward_end_of_room(self):
        bonus = self.player.coins // 10
        self.player.coins += bonus
        self.player.coins += int(self.player.health)
        time_coins = 5
        time_coins -= int(self.room_time/time_coins)
        if time_coins > 0:
            self.player.coins += time_coins         

    def update(self, dt):
        self.update_player(dt)
        self.update_player_shooting()
        self.update_projectiles(dt)
        self.update_enemies(dt)
        self.resolve_collisions()
        self.check_game_over()
        self.is_complete()
        self.update_items()
        self.update_triggers()
        self.check_next_trigger()
        if not self.complete:
            self.room_time += dt
        
