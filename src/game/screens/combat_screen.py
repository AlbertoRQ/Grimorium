import pygame

from game import config
from game.rooms.room import Room
from game.screens.base_screen import BaseScreen
from game.ui.fonts import create_font
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

ELEMENTS_KEYS = {
    pygame.K_4: None,
    pygame.K_5: "fire",
    pygame.K_6: "ice",
    pygame.K_7: "electric",
}


class CombatScreen(BaseScreen):
    VIRTUAL_WIDTH = 640
    VIRTUAL_HEIGHT = 360
    def __init__(self, game, room_layout, room_type):
        super().__init__(game)

        self.player = self.game.player
        self.player.visual.set_size(32, 32)
        self.player.visual.clear_fixed_frame()
        self.player.visual.set_locked(False)
        self.player.visual.set_state("idle", reset=True)
        self.player.visual.set_facing("down")
        self.bullets = []
        self.enemies = []
        self.enemies_bullets = []
        self.font = create_font(3)

        self.room = Room(room_layout, room_type, self.VIRTUAL_WIDTH, self.VIRTUAL_HEIGHT)
        self.place_player_at_spawn()

        self.complete = False
        self.items = []
        self.items_spawned = False
        self.reward_item_count = 3

        self.triggers = []
        self.triggers_spawned = False

        self.room_time = 0

        self.stat_positions = {
            "coins": (25, 60),
            "health": (25, 85),
            "damage": (25, 110),
            "speed": (25, 135),
            "fire_rate": (25, 160),
            "shoot_distance": (25, 185),
            "body_damage": (25, 210),
            "luck": (25, 235),
        }

    def get_blockers(self, include_walls=True, include_objects=True, include_voids=False):
        return self.room.get_blocking_rects(include_walls, include_objects, include_voids)

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
        if key in ELEMENTS_KEYS:
            self.player.bullet_element = ELEMENTS_KEYS[key]

    def kill_all_enemies(self):
        self.enemies = []

    def update_player(self, dt, blockers):
        keys = pygame.key.get_pressed()
        self.player.move(keys, dt, blockers, [])
        self.player.update(dt)

    def update_player_shooting(self):
        keys = pygame.key.get_pressed()
        self.bullets.extend(self.player.shoot(keys))

    def update_enemies(self, dt, blockers):
        for enemy in self.enemies:
            new_bullets = enemy.update(self.player, dt, blockers, self.enemies)

            if new_bullets:
                self.enemies_bullets.extend(new_bullets)

    def update_projectiles(self, dt, blockers):
        blockers = self.get_blockers(True, True, False)

        for bullet in self.bullets:
            bullet.update(dt, blockers)

        for enemy_bullet in self.enemies_bullets:
            enemy_bullet.update(dt, blockers)

        self.bullets = [
            bullet for bullet in self.bullets
            if not bullet.is_offscreen() and not bullet.destroyed
        ]

        self.enemies_bullets = [
            bullet for bullet in self.enemies_bullets
            if not bullet.is_offscreen() and not bullet.destroyed
        ]


    def resolve_collisions(self, blockers):
        self.bullets, self.enemies, coins_gained = resolve_player_bullets_vs_enemies(
            self.bullets,
            self.enemies,
            blockers,
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
            blockers
        )
        self.player.coins += coins_gained

    def remove_dead_enemies(self):
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead()]

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
        x = 25
        y = 40
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

        self.player.draw_player_stats(surface, self.font, self.stat_positions)
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
        max_bonus = 3
        bonus = min(self.player.coins // 15, max_bonus)

        self.player.coins += bonus
        self.player.coins += int(self.player.health) // 2

        time_coins = 5
        time_coins -= int(self.room_time / time_coins)
        if time_coins > 0:
            self.player.coins += time_coins       

    def update(self, dt):
        blockers_full = self.get_blockers(True, True, True)
        blockers_projectiles = self.get_blockers(True, True, False)

        self.update_player(dt, blockers_full)
        self.update_player_shooting()
        self.update_projectiles(dt, blockers_projectiles)
        self.update_enemies(dt, blockers_full)
        self.remove_dead_enemies()
        self.resolve_collisions(blockers_full)
        self.check_game_over()
        self.is_complete()
        self.update_items()
        self.update_triggers()
        self.check_next_trigger()
        if not self.complete:
            self.room_time += dt
        
