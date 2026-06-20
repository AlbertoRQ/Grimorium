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

from game.utils.paths import asset_path

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

        # Combat background
        self.background = pygame.image.load(asset_path("images", "combat_screen.png")).convert()
        self.background_original_size = self.background.get_size()

        self.base_width, self.base_height = self.background_original_size

        self.pixel_scale = min(
            self.VIRTUAL_WIDTH // self.base_width,
            self.VIRTUAL_HEIGHT // self.base_height,
        )

        self.render_width = self.base_width * self.pixel_scale
        self.render_height = self.base_height * self.pixel_scale
        self.offset_x = (self.VIRTUAL_WIDTH - self.render_width) // 2
        self.offset_y = (self.VIRTUAL_HEIGHT - self.render_height) // 2

        self.background = pygame.transform.scale(
            self.background,
            (self.render_width, self.render_height)
        )



        self.player = self.game.player
        self.player.visual.set_size(32, 32)
        self.player.visual.clear_fixed_frame()
        self.player.visual.set_locked(False)
        self.player.visual.set_state("idle", reset=True)
        self.player.visual.set_facing("down")
        self.bullets = []
        self.enemies = []
        self.enemies_bullets = []
        self.font = create_font(9)

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
            "coins": (58, 97),
            "health": (0, 0),
            "damage": (60, 121),
            "speed": (60, 143),
            "fire_rate": (60, 163),
            "shoot_distance": (60, 183),
            "body_damage": (60, 205),
            "luck": (0, 0),
        }

        self.floor_track_rooms = [
            step for step in config.RUN_PATTERN
            if step != "shop"
        ]

        self.floor_track_images = {
            "normal": pygame.image.load(
                asset_path("images", "floor_track", "normal_floor.png")
            ).convert_alpha(),
            "boss": pygame.image.load(
                asset_path("images", "floor_track", "boss_floor.png")
            ).convert_alpha(),
            "shop": pygame.image.load(
                asset_path("images", "floor_track", "shop_floor.png")
            ).convert_alpha(),
        }

        self.floor_track_floor_positions  = [
            (595, 240),
            (595, 217),
            (595, 194),
            (595, 171),
            (595, 148),
            (595, 125),
        ]

        self.floor_track_shop_positions = [
            (595, 228),
            (595, 205),
            (595, 182),
            (595, 159),
            (595, 136),
        ]

        self.floor_track_shop_indices = self.build_floor_track_shops()
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
        surface.blit(self.background, (self.offset_x, self.offset_y))

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

        max_floors = sum(1 for step in config.RUN_PATTERN if step == "normal" or step == "boss")
        current_floor = self.game.room_level

        current_loop = self.game.run_cycles + 1
        max_loops = self.game.max_cycles

        time_text = self.font.render(f"Time: {self.room_time:.1f}", True, config.HUD_COLOR)
        time_rect = time_text.get_rect(center=(53, 55))
        surface.blit(time_text, time_rect)


        floor_text = self.font.render(f"FLOOR", True, config.HUD_COLOR)
        floor_rect = floor_text.get_rect(center=(595, 271))
        surface.blit(floor_text, floor_rect)

        floor_num = self.font.render(f"{current_floor}/{max_floors}", True, config.HUD_COLOR)
        floor_num_rect = floor_num.get_rect(center=(595, 285))
        surface.blit(floor_num, floor_num_rect)


        loop_text = self.font.render(f"LOOP", True, config.HUD_COLOR)
        loop_rect = loop_text.get_rect(center=(595, 307))        
        surface.blit(loop_text, loop_rect)

        loop_num = self.font.render(f"{current_loop}/{max_loops}", True, config.HUD_COLOR)
        loop_num_rect = loop_num.get_rect(center=(595, 321))        
        surface.blit(loop_num, loop_num_rect)


        for index, room_type in enumerate(self.floor_track_rooms):
            image = self.floor_track_images[room_type]
            rect = image.get_rect(center=self.floor_track_floor_positions[index])
            surface.blit(image, rect)

        for shop_index in self.floor_track_shop_indices:
            if shop_index >= len(self.floor_track_shop_positions):
                continue

            image = self.floor_track_images["shop"]
            rect = image.get_rect(center=self.floor_track_shop_positions[shop_index])
            surface.blit(image, rect)

        marker_pos = self.get_floor_track_marker_position()

        pygame.draw.circle(surface, (0, 0, 0), marker_pos, 6)
        pygame.draw.circle(surface, (255, 255, 255), marker_pos, 4)

        

        self.draw_extra(surface)
        self.draw_hud(surface)

    def draw_extra(self, surface):
        pass

    def draw_hud(self, surface):

        self.player.draw_player_stats(surface, self.font, self.stat_positions)
        self.player.draw_player_health(surface, self.font)
        self.player.draw_player_items(surface, self.font)

    def get_current_floor_track_index(self):
        combat_index = 0

        for index, step in enumerate(config.RUN_PATTERN):
            if step == "shop":
                continue

            if index == self.game.current_step_index:
                return combat_index

            combat_index += 1

        return 0
        
    def get_floor_track_marker_position(self):
        current_index = self.get_current_floor_track_index()
        x, y = self.floor_track_floor_positions[current_index]
        return (x - 18, y)
    
    def build_floor_track_shops(self):
        shops_between_rooms = []
        room_count = 0

        for step in config.RUN_PATTERN:
            if step in ("normal", "boss"):
                room_count += 1
                continue

            if step == "shop":
                # Solo cuenta si está entre dos rooms del track
                if 0 < room_count < len(self.floor_track_rooms):
                    shops_between_rooms.append(room_count - 1)

        return shops_between_rooms


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
        
