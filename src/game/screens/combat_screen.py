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
from game.systems.voltaic_fragmentation import VoltaicFragmentation
from game.systems.poison_cloud import PoisonCloud
from game.systems.lava_drop import LavaDrop
from game.systems.ice_puddle import IcePuddle
from game.systems.toxic_overload import ToxicOverload
from game.systems.toxic_trail import ToxicTrail
from game.entities.bullets.bullet import Bullet

from game.entities.triggers.trigger import Trigger

from game.utils.paths import asset_path

WEAPON_KEYS = {
    pygame.K_1: "normal",
    pygame.K_2: "gatling",
    pygame.K_3: "spread",
}



class CombatScreen(BaseScreen):
    VIRTUAL_WIDTH = 640
    VIRTUAL_HEIGHT = 360
    def __init__(self, game, room_layout, room_type):
        super().__init__(game)

        # Combat background
        self.setup_background()

        self.setup_player_for_combat()

        self.bullets = []
        self.combat_effects = []
        self.voltaic_fragmentations = []
        self.ice_puddles = []
        self.poison_clouds = []
        self.lava_drops = []
        self.toxic_overload = None
        self.toxic_trail = None

        self.enemies = []
        self.enemies_bullets = []
        self.font = create_font(9)

        self.room = Room(room_layout, room_type, self.VIRTUAL_WIDTH, self.VIRTUAL_HEIGHT)
        self.place_player_at_spawn()

        self.complete = False

        self.triggers = []
        self.triggers_spawned = False

        self.intro_active = True
        self.intro_speed = 70
        self.setup_room_intro()
        
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

        self.setup_floor_track()


    def setup_background(self):
        self.background = pygame.image.load(
            asset_path("images", "combat_screen.png")
        ).convert()
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
            (self.render_width, self.render_height),
        )

    def setup_player_for_combat(self):
        self.player = self.game.player
        self.player.visual.set_size(32, 32)
        self.player.visual.clear_fixed_frame()
        self.player.visual.set_locked(False)
        self.player.visual.set_state("idle", reset=True)
        self.player.visual.set_facing("down")

    
    def setup_floor_track(self):
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

        self.floor_track_floor_positions = [
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
    

    def setup_room_intro(self):
        if self.room.player_spawn is None:
            self.intro_active = False
            return

        entrance_door = self.room.get_entrance_door()

        if entrance_door is None:
            self.intro_active = False
            return

        self.intro_target_x, self.intro_target_y = self.get_intro_target_from_door(entrance_door)

        self.player.x = entrance_door["full_rect"].centerx
        self.player.y = entrance_door["full_rect"].centery

        self.player.visual.set_facing("up")
        self.player.visual.set_state("walk", reset=True)

    
    def get_intro_target_from_door(self, door):
        x = door["full_rect"].centerx
        y = door["full_rect"].centery
        distance = config.ROOM_CELL_SIZE

        if door["side"] == "bottom":
            y -= distance
        elif door["side"] == "top":
            y += distance
        elif door["side"] == "left":
            x += distance
        elif door["side"] == "right":
            x -= distance

        return x, y

    def update_room_intro(self, dt):
        dx = self.intro_target_x - self.player.x
        dy = self.intro_target_y - self.player.y

        distance = (dx * dx + dy * dy) ** 0.5

        if distance <= 2:
            self.player.x = self.intro_target_x
            self.player.y = self.intro_target_y
            self.player.visual.set_state("idle", reset=True)
            self.room.close_entrance_doors()
            self.intro_active = False
            return

        self.player.x += dx / distance * self.intro_speed * dt
        self.player.y += dy / distance * self.intro_speed * dt
        self.player.visual.update(dt)

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

    def update_player(self, dt, blockers):
        keys = pygame.key.get_pressed()
        self.player.move(keys, dt, blockers, [])
        self.player.update(dt)

    def update_player_shooting(self):
        keys = pygame.key.get_pressed()
        new_bullets = self.player.shoot(keys)

        bullets_to_fire = []

        for bullet in new_bullets:
            elements = set(bullet.elements)
            is_toxic_overload_bullet = (
                "electric" in elements
                and "poison" in elements
            )

            if is_toxic_overload_bullet:
                if self.toxic_overload is None:
                    combo_data = bullet.effect_data["combos"]["electric_poison"]

                    self.toxic_overload = ToxicOverload(
                        self.player,
                        combo_data,
                    )

                    if combo_data["trail_enabled"]:
                        if self.toxic_trail is None:
                            self.toxic_trail = ToxicTrail(
                                combo_data,
                                bullet.effect_data,
                            )

                    self.player.toxic_overload_active = True
                    self.player.toxic_overload_speed_multiplier = (
                        self.toxic_overload.speed_multiplier
                    )

                # Esta bala se consume y no se añade a bullets_to_fire.
                continue

            bullets_to_fire.append(bullet)

        self.bullets.extend(bullets_to_fire)

    def update_enemies(self, dt, blockers):
        wall_blockers = self.get_blockers(True, False, False)

        for enemy in self.enemies:
            enemy_blockers = wall_blockers if getattr(enemy, "is_flying", False) else blockers
            new_bullets = enemy.update(self.player, dt, enemy_blockers, self.enemies, self.room)

            if new_bullets:
                self.enemies_bullets.extend(new_bullets)

    def update_projectiles(self, dt, blockers):
        blockers = self.get_blockers(True, True, False)

        for bullet in self.bullets:
            bullet.update(dt, blockers)
            self.ignite_poison_clouds(bullet)

            if bullet.hit_wall and self.has_voltaic_fragmentation(bullet):
                original_damage = bullet.damage * self.player.damage

                effect = VoltaicFragmentation(
                    bullet,
                    original_damage,
                    can_refragment=self.has_voltaic_refragmentation(bullet),
                )

                self.voltaic_fragmentations.append(effect)

            elif bullet.hit_wall and bullet.can_refragment:
                original_damage = bullet.damage * self.player.damage

                effect = VoltaicFragmentation(
                    bullet,
                    original_damage,
                    is_refragmentation=True,
                )

                self.voltaic_fragmentations.append(effect)

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
        self.bullets, self.enemies, coins_gained, created_effects = resolve_player_bullets_vs_enemies(
            self.bullets,
            self.enemies,
            blockers,
            self.player.damage,
        )
        self.player.coins += coins_gained

        for effect in created_effects:
            if isinstance(effect, Bullet):
                self.bullets.append(effect)
            elif isinstance(effect, IcePuddle):
                self.ice_puddles.append(effect)
            elif isinstance(effect, PoisonCloud):
                self.poison_clouds.append(effect)
            else:
                self.combat_effects.append(effect)

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

        self.draw_world(surface)
        self.draw_entities(surface)
        self.draw_projectiles(surface)
        self.draw_effects(surface)
        self.draw_room_info(surface)
        self.draw_floor_track(surface)

        self.draw_extra(surface)
        self.draw_hud(surface)

    def draw_world(self, surface):
        self.room.draw(surface)

        if self.toxic_trail is not None:
            self.toxic_trail.draw(surface)

        if self.toxic_overload is not None:
            self.toxic_overload.draw(surface)

        for puddle in self.ice_puddles:
            puddle.draw(surface)

        # for trigger in self.triggers:
        #     trigger.draw(surface)

    def draw_entities(self, surface):
        self.player.draw(surface)

        for enemy in self.enemies:
            enemy.draw(surface)

    def draw_projectiles(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

        for enemy_bullet in self.enemies_bullets:
            enemy_bullet.draw(surface)

    def draw_effects(self, surface):
        for cloud in self.poison_clouds:
            cloud.draw(surface)

        for lava_drop in self.lava_drops:
            lava_drop.draw(surface)

        for effect in self.voltaic_fragmentations:
            effect.draw(surface)

        for effect in self.combat_effects:
            effect.draw(surface)

    def draw_room_info(self, surface):
        max_floors = sum(1 for step in config.RUN_PATTERN if step in ("normal", "boss"))
        current_floor = self.game.room_level

        current_loop = self.game.run_cycles + 1
        max_loops = self.game.max_cycles

        time_text = self.font.render(f"Time: {self.room_time:.1f}", True, config.HUD_COLOR)
        time_rect = time_text.get_rect(center=(53, 55))
        surface.blit(time_text, time_rect)

        floor_text = self.font.render("FLOOR", True, config.HUD_COLOR)
        floor_rect = floor_text.get_rect(center=(595, 271))
        surface.blit(floor_text, floor_rect)

        floor_num = self.font.render(f"{current_floor}/{max_floors}", True, config.HUD_COLOR)
        floor_num_rect = floor_num.get_rect(center=(595, 285))
        surface.blit(floor_num, floor_num_rect)

        loop_text = self.font.render("LOOP", True, config.HUD_COLOR)
        loop_rect = loop_text.get_rect(center=(595, 307))
        surface.blit(loop_text, loop_rect)

        loop_num = self.font.render(f"{current_loop}/{max_loops}", True, config.HUD_COLOR)
        loop_num_rect = loop_num.get_rect(center=(595, 321))
        surface.blit(loop_num, loop_num_rect)


    def draw_floor_track(self, surface):
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


    def draw_extra(self, surface):
        pass

    def draw_hud(self, surface):

        self.player.draw_player_stats(surface, self.font, self.stat_positions)
        self.player.draw_player_health(surface, self.font)

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
    
    def update_completion_state(self):
        if self.complete:
            return

        if len(self.enemies) == 0:
            self.complete = True


    def spawn_triggers(self):
        for trigger_rect in self.room.trigger_spawns:
            self.triggers.append(Trigger(trigger_rect))

    def update_triggers(self):
        if not self.complete:
            return

        if not self.triggers_spawned:
            self.room.open_doors()
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

    def update_combat_effects(self, dt):
        new_effects = []

        for effect in self.combat_effects:
            created_effects = effect.update(dt, self.enemies)

            if created_effects:
                new_effects.extend(created_effects)

        self.combat_effects = [
            effect for effect in self.combat_effects
            if not effect.finished
        ]

        self.combat_effects.extend(new_effects)


    def has_voltaic_fragmentation(self, bullet):
        required_elements = {"fire", "electric"}

        return (
            required_elements.issubset(set(bullet.elements))
            and bullet.can_fragment
        )

    def has_voltaic_refragmentation(self, bullet):
        combo_data = bullet.effect_data.get("combos", {}).get(
            "fire_electric",
            {},
        )
        return combo_data.get("refragment_divisor", 0) > 0
    

    def update_voltaic_fragmentations(self, dt):
        new_fragments = []

        for effect in self.voltaic_fragmentations:
            fragments = effect.update(dt)
            new_fragments.extend(fragments)

        self.voltaic_fragmentations = [
            effect
            for effect in self.voltaic_fragmentations
            if not effect.finished
        ]

        self.bullets.extend(new_fragments)

    def update_ice_puddles(self, dt):
        for enemy in self.enemies:
            enemy.puddle_slow_multiplier = 1.0

        for puddle in self.ice_puddles:
            puddle.update(dt, self.enemies)

        self.ice_puddles = [
            puddle for puddle in self.ice_puddles
            if not puddle.finished
        ]

    def update_poison_clouds(self, dt):
        new_lava_drops = []

        for cloud in self.poison_clouds:
            new_lava_drops.extend(cloud.update(dt, self.enemies))

        self.poison_clouds = [
            cloud for cloud in self.poison_clouds
            if not cloud.expired
        ]

        self.lava_drops.extend(new_lava_drops)

        for lava_drop in self.lava_drops:
            lava_drop.update(dt, self.enemies)

        self.lava_drops = [
            lava_drop for lava_drop in self.lava_drops
            if not lava_drop.finished
        ]

    def ignite_poison_clouds(self, bullet):
        if "fire" not in bullet.elements:
            return

        fire_data = bullet.effect_data.get("fire")

        for cloud in self.poison_clouds:
            if cloud.contains_entity(bullet):
                cloud.ignite(fire_data)

    def electrify_ice_puddles(self):
        for bullet in self.bullets:
            if "electric" not in bullet.elements:
                continue

            for puddle in self.ice_puddles:
                if puddle.contains_entity(bullet):
                    puddle.electrify()

    def update_toxic_overload(self, dt):
        if self.toxic_overload is not None:
            self.toxic_overload.update(dt, self.enemies)

            if self.toxic_overload.finished:
                self.toxic_overload = None
                self.player.toxic_overload_active = False
                self.player.toxic_overload_speed_multiplier = 1.0

    def update_toxic_trail(self, dt):
        if self.toxic_trail is None:
            return

        player = self.player if self.toxic_overload is not None else None
        self.toxic_trail.update(dt, self.enemies, player)

        if self.toxic_trail.finished:
            self.toxic_trail = None
    

    def update_player_phase(self, dt, blockers):
        self.update_player(dt, blockers)
        self.update_player_shooting()
        
    def update_projectile_phase(self, dt, blockers):
        self.update_projectiles(dt, blockers)
        self.electrify_ice_puddles()
        self.update_voltaic_fragmentations(dt)

    def update_enemy_phase(self, dt, blockers):
        self.update_enemies(dt, blockers)
        self.remove_dead_enemies()
        self.resolve_collisions(blockers)

    def update_effect_phase(self, dt):
        self.update_toxic_overload(dt)
        self.update_toxic_trail(dt)
        self.update_ice_puddles(dt)
        self.update_poison_clouds(dt)
        self.update_combat_effects(dt)

    def update_room_state_phase(self):
        self.check_game_over()
        self.update_completion_state()
        self.update_triggers()
        self.check_next_trigger()

    def update_room_timer(self, dt):
        if not self.complete:
            self.room_time += dt

    def update(self, dt):

        if self.intro_active:
            self.update_room_intro(dt)
            return
        
        blockers_full = self.get_blockers(True, True, True)
        blockers_projectiles = self.get_blockers(True, True, False)

        self.update_player_phase(dt, blockers_full)
        self.update_projectile_phase(dt, blockers_projectiles)
        self.update_enemy_phase(dt, blockers_full)
        self.update_effect_phase(dt)
        self.update_room_state_phase()
        self.update_room_timer(dt)
        
