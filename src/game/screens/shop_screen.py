import pygame
import random

from game import config
from game.screens.base_screen import BaseScreen
from game.ui.fonts import create_font

from game.utils.paths import asset_path

class ShopScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.player = self.game.player

        # Shop background
        self.background = pygame.image.load(asset_path("images", "shop.bmp")).convert()
        self.background_original_size = self.background.get_size()

        self.base_width, self.base_height = self.background_original_size
        self.pixel_scale = min(
            config.SCREEN_WIDTH // self.base_width,
            config.SCREEN_HEIGHT // self.base_height,
        )
        self.pixel_scale = max(1, self.pixel_scale)
        self.render_width = self.base_width * self.pixel_scale
        self.render_height = self.base_height * self.pixel_scale
        self.offset_x = (config.SCREEN_WIDTH - self.render_width) // 2
        self.offset_y = (config.SCREEN_HEIGHT - self.render_height) // 2


        self.background = pygame.transform.scale(
            self.background,
            (self.render_width, self.render_height)
        )

        self.title_font = create_font(pixel_scale=self.pixel_scale)
        self.info_font = create_font(pixel_scale=self.pixel_scale)


        self.player.x = self.offset_x + 205 * self.pixel_scale
        self.player.y = self.offset_y + 124 * self.pixel_scale
        self.player.sprite_size_x = 32 * self.pixel_scale
        self.player.sprite_size_y = 32 * self.pixel_scale  
        

        self.shop_slots = {
            "potions": [
                (129, 51), (149, 51), (169, 51), (189, 51),
                (129, 84), (149, 84), (169, 84), (189, 84),
            ],
            "books": [
                (232, 45), (264, 45),
                (232, 67), (264, 67),
                (232, 89), (264, 89),
            ],
            "powers": [
                (55, 49), (87, 49),
                (55, 84), (87, 84),
            ],
        }
        

        # Potions
        potion_size = (32 * self.pixel_scale, 32 * self.pixel_scale)

        self.loaded_potions = []

        for image_path in asset_path("images", "potions").glob("potion_*.*"):
            potion_id = image_path.stem.removeprefix("potion_")

            image = pygame.image.load(str(image_path)).convert()
            image.set_colorkey((0, 0, 0))
            image = pygame.transform.scale(image, potion_size)

            self.loaded_potions.append({
                "id": potion_id,
                "image": image,
                "path": str(image_path),
            })
        
        self.potions_in_shop = []
        

        for slot in self.shop_slots["potions"]:
            potion_data = random.choice(self.loaded_potions)

            rect = self.build_layout_rect(self.shop_slots["potions"][len(self.potions_in_shop)], (32, 32))

            self.potions_in_shop.append({
                "id": potion_data["id"],
                "image": potion_data["image"],
                "price": config.POTION_DATA[potion_data["id"]]["price"],
                "rect": rect,
            })


        # Books
        book_size = (32 * self.pixel_scale, 32 * self.pixel_scale)

        self.loaded_books = []

        for image_path in asset_path("images", "books").glob("book_*.*"):
            book_id = image_path.stem.removeprefix("book_")

            image = pygame.image.load(str(image_path)).convert()
            image.set_colorkey((0, 147, 71))
            image = pygame.transform.scale(image, book_size)

            self.loaded_books.append({
                "id": book_id,
                "image": image,
                "path": str(image_path),
            })
        
        self.books_in_shop = []

        for slot in self.shop_slots["books"]:
            book_data = random.choice(self.loaded_books)

            rect = self.build_layout_rect(self.shop_slots["books"][len(self.books_in_shop)], (32, 32))

            self.books_in_shop.append({
                "id": book_data["id"],
                "image": book_data["image"],
                "price": config.BOOK_DATA[book_data["id"]]["price"],
                "rect": rect,
            })

        # Powers
        power_size = (32 * self.pixel_scale, 32 * self.pixel_scale)

        self.loaded_powers = []

        for image_path in asset_path("images", "powers").glob("power_*.*"):
            power_id = image_path.stem.removeprefix("power_")

            image = pygame.image.load(str(image_path)).convert()
            image.set_colorkey((0, 147, 0))
            image = pygame.transform.scale(image, power_size)

            self.loaded_powers.append({
                "id": power_id,
                "image": image,
                "path": str(image_path),
            })
        
        self.powers_in_shop = []

        for slot in self.shop_slots["powers"]:
            power_data = random.choice(self.loaded_powers)

            rect = self.build_layout_rect(self.shop_slots["powers"][len(self.powers_in_shop)], (32, 32))

            self.powers_in_shop.append({
                "id": power_data["id"],
                "image": power_data["image"],
                "price": config.POWER_DATA[power_data["id"]]["price"],
                "rect": rect,
            })

        self.price_powers = pygame.image.load(asset_path("images", "prices", f"price_{config.POWER_PRICE}.png")).convert_alpha()
        self.price_potions = pygame.image.load(asset_path("images", "prices", f"price_{config.POTION_PRICE}.png")).convert_alpha()
        self.price_books = pygame.image.load(asset_path("images", "prices", f"price_{config.BOOK_PRICE}.png")).convert_alpha()

        price_size = (19 * self.pixel_scale, 11 * self.pixel_scale)

        self.price_powers = pygame.transform.scale(self.price_powers, price_size)
        self.price_potions = pygame.transform.scale(self.price_potions, price_size)
        self.price_books = pygame.transform.scale(self.price_books, price_size)

        self.price_positions = {
            "powers": (70, 105),
            "potions": (158, 105),
            "books": (248, 105),
        }

        self.stat_positions = {
            "coins": (208, 144),
            "health": (177, 117),
            "damage": (177, 124),
            "speed": (177, 132),
            "fire_rate": (241, 117),
            "shoot_distance": (241, 124),
            "body_damage": (241, 132),
            "luck": (0, 0),
        }

        self.scaled_stat_positions = {
            key: self.scale_layout_point(point)
            for key, point in self.stat_positions.items()
        }

        self.level_book_images = {}

        for image_path in asset_path("images", "level_books").glob("*.png"):
            level_id = image_path.stem

            image = pygame.image.load(str(image_path)).convert_alpha()
            image = pygame.transform.scale(image, (25 * self.pixel_scale, 10 * self.pixel_scale))

            self.level_book_images[level_id] = image

        self.level_book_positions = {
            "lvl_fire": (166, 156),
            "lvl_ice": (193, 156),
            "lvl_fire_ice": (166, 168),
        }

        self.level_text_positions = {
            "fire": (169, 156),
            "ice": (196, 156),
            "fire_ice": (169, 168),
        }

        self.scaled_level_text_positions = {
            key: self.scale_mixed_layout_point(point)
            for key, point in self.level_text_positions.items()
        }

    def buy_potion(self, potion):
        if self.player.coins < potion["price"]:
            return
        
        self.apply_potion_effect(potion["id"])
        self.player.coins -= potion["price"]
        self.potions_in_shop.remove(potion)

    def apply_potion_effect(self, potion_id):
        potion_data = config.POTION_DATA[potion_id]
        stat = potion_data["stat"]
        amount = potion_data["amount"]

        if stat == "health":
            self.player.health = min(self.player.max_health, self.player.health + amount)
            return

        current_value = getattr(self.player, stat)
        setattr(self.player, stat, current_value + amount)

    def buy_book(self, book):
        if self.player.coins < book["price"]:
            return
        
        self.apply_book_effect(book["id"])
        self.player.coins -= book["price"]
        self.books_in_shop.remove(book)

    def apply_book_effect(self, book_id):
        effect = config.BOOK_DATA[book_id]["effect"]

        if "combo" in effect:
            combo = effect["combo"]

            for stat, bonus in effect.items():
                if stat == "combo":
                    continue

                self.player.combo_stats[combo][stat] += bonus
            return

        element = effect["element"]

        for stat, bonus in effect.items():
            if stat == "element":
                continue

            self.player.element_stats[element][stat] += bonus
            
    def buy_power(self, power):
        if self.player.coins < power["price"]:
            return

        self.apply_power_effect(power["id"])
        self.player.coins -= power["price"]
        self.powers_in_shop.remove(power)

    def apply_power_effect(self, power_id):
        power_data = config.POWER_DATA[power_id]
        element = power_data["element"]

        if power_data["mode"] == "base":
            if element not in self.player.base_bullet_elements:
                self.player.base_bullet_elements.append(element)
        else:
            self.player.extra_bullet_element[element] = power_data["chance"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.go_to_next_run_screen()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            for potion in self.potions_in_shop[:]:
                if potion["rect"].collidepoint(mouse_pos):
                    self.buy_potion(potion)
                    break

            for power in self.powers_in_shop[:]:
                if power["rect"].collidepoint(mouse_pos):
                    self.buy_power(power)
                    break

            for book in self.books_in_shop[:]:
                if book["rect"].collidepoint(mouse_pos):
                    self.buy_book(book)
                    break

    def draw(self, surface):
        surface.blit(self.background, (self.offset_x, self.offset_y))

        for potion in self.potions_in_shop:
            surface.blit(potion["image"], potion["rect"])

        for book in self.books_in_shop:
            surface.blit(book["image"], book["rect"])

        for power in self.powers_in_shop:
            surface.blit(power["image"], power["rect"])

        self.player.set_fixed_frame(2, 0)
        self.player.draw(surface)

        self.player.draw_player_stats(surface, self.info_font, self.scaled_stat_positions)

        rect_price_powers = self.price_powers.get_rect(center=self.scale_layout_point(self.price_positions["powers"]))
        surface.blit(self.price_powers, rect_price_powers)

        rect_price_potions = self.price_potions.get_rect(center=self.scale_layout_point(self.price_positions["potions"]))
        surface.blit(self.price_potions, rect_price_potions)

        rect_price_books = self.price_books.get_rect(center=self.scale_layout_point(self.price_positions["books"]))
        surface.blit(self.price_books, rect_price_books)

        for level_id, base_pos in self.level_book_positions.items():
            image = self.level_book_images[level_id]
            rect = self.build_mixed_layout_rect(base_pos, (25, 10))
            surface.blit(image, rect)

        level_texts = {
            "fire": f"lv:{self.player.element_stats['fire']['level']}",
            "ice": f"lv:{self.player.element_stats['ice']['level']}",
            "fire_ice": f"lv:{self.player.combo_stats['fire_ice']['level']}",
        }

        for key, text_value in level_texts.items():
            text = self.info_font.render(text_value, True, config.HUD_COLOR)
            cx, cy = self.scaled_level_text_positions[key]

            text_rect = text.get_rect()
            text_rect.x = cx - text_rect.width // 2
            text_rect.y = cy - text_rect.height // 2

            surface.blit(text, text_rect)


    def scale_layout_point(self, base_point):
        return (
            self.offset_x + base_point[0] * self.pixel_scale + self.pixel_scale // 2,
            self.offset_y + base_point[1] * self.pixel_scale + self.pixel_scale // 2,
        )
    
    def scale_mixed_layout_point(self, base_point):
        return (
            self.offset_x + base_point[0] * self.pixel_scale + self.pixel_scale // 2,
            self.offset_y + base_point[1] * self.pixel_scale,
        )
    
    def build_layout_rect(self, base_center, base_size):
        width = base_size[0] * self.pixel_scale
        height = base_size[1] * self.pixel_scale

        rect = pygame.Rect(0, 0, width, height)
        rect.x = self.offset_x + base_center[0] * self.pixel_scale - rect.width // 2
        rect.y = self.offset_y + base_center[1] * self.pixel_scale - rect.height // 2
        return rect

    def build_mixed_layout_rect(self, base_center, base_size):
        width = base_size[0] * self.pixel_scale
        height = base_size[1] * self.pixel_scale

        rect = pygame.Rect(0, 0, width, height)
        rect.x = self.offset_x + base_center[0] * self.pixel_scale + self.pixel_scale // 2 - rect.width // 2
        rect.y = self.offset_y + base_center[1] * self.pixel_scale - rect.height // 2
        return rect