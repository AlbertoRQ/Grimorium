import pygame
import random

from game import config
from game.screens.base_screen import BaseScreen
from pathlib import Path

from game.utils.paths import asset_path



class ShopScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.player = self.game.player
        self.title_font = pygame.font.Font(None, 72)
        self.info_font = pygame.font.Font(None, 36)

        # Shop background
        self.background = pygame.image.load(asset_path("images", "shop.bmp")).convert()
        self.background_original_size = self.background.get_size()

        self.background = pygame.transform.scale(
            self.background,
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        self.scale_x = config.SCREEN_WIDTH / self.background_original_size[0]
        self.scale_y = config.SCREEN_HEIGHT / self.background_original_size[1]

        self.player.x, self.player.y = self.scale_point((164,124))
        self.player.sprite_size_x = 32 * self.scale_x
        self.player.sprite_size_y = 32 * self.scale_y  
        self.player.sprite = self.player.get_frame(2, 0)
        self.player.sprite = pygame.transform.scale(self.player.sprite, (self.player.sprite_size_x, self.player.sprite_size_y))

        self.shop_slots = {
            "potions": [(113, 42),(133, 42),(153, 42),(173, 42),
                        (113, 75),(133, 75),(153, 75),(173, 75)],
            "books": [(216, 36),(248, 36),
                      (216, 58),(248, 58),
                      (216, 80),(248, 80)],
            "powers": [(39, 40),(71, 40),
                      (39, 75),(71, 75)]
        }
        
        self.scaled_shop_slots = {
            category: [self.scale_point(point) for point in points]
            for category, points in self.shop_slots.items()
        }

        # Potions
        potion_base_size = (32, 32)
        potion_size = (
            int(potion_base_size[0] * self.scale_x),
            int(potion_base_size[1] * self.scale_y),
        )

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

        for slot in self.scaled_shop_slots["potions"]:
            potion_data = random.choice(self.loaded_potions)

            self.potions_in_shop.append({
                "id": potion_data["id"],
                "image": potion_data["image"],
                "price": config.POTION_DATA[potion_data["id"]]["price"],
                "rect": potion_data["image"].get_rect(center=slot),
            })


        # Books
        book_base_size = (32, 32)
        book_size = (
            int(book_base_size[0] * self.scale_x),
            int(book_base_size[1] * self.scale_y),
        )

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

        for slot in self.scaled_shop_slots["books"]:
            book_data = random.choice(self.loaded_books)

            self.books_in_shop.append({
                "id": book_data["id"],
                "image": book_data["image"],
                "price": config.BOOK_DATA[book_data["id"]]["price"],
                "rect": book_data["image"].get_rect(center=slot),
            })

        # Powers
        power_base_size = (32, 32)
        power_size = (
            int(power_base_size[0] * self.scale_x),
            int(power_base_size[1] * self.scale_y),
        )

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

        for slot in self.scaled_shop_slots["powers"]:
            power_data = random.choice(self.loaded_powers)

            self.powers_in_shop.append({
                "id": power_data["id"],
                "image": power_data["image"],
                "price": config.POWER_DATA[power_data["id"]]["price"],
                "rect": power_data["image"].get_rect(center=slot),
            })

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
        surface.blit(self.background, (0, 0))

        for potion in self.potions_in_shop:
            surface.blit(potion["image"], potion["rect"])

        for book in self.books_in_shop:
            surface.blit(book["image"], book["rect"])

        for power in self.powers_in_shop:
            surface.blit(power["image"], power["rect"])

        self.player.draw(surface)

        x, y = self.scale_point((188,100))
        self.player.draw_player_stats(surface, self.info_font, x, y)


        # title = self.title_font.render("Tienda", True, config.HUD_COLOR)
        # info = self.info_font.render("Placeholder - Pulsa Enter para continuar", True, config.HUD_COLOR)
        # coins = self.info_font.render(f"Monedas: {self.player.coins}", True, config.HUD_COLOR)

        # surface.blit(title, title.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 60)))
        # surface.blit(info, info.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)))
        # surface.blit(coins, coins.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 50)))

    def scale_point(self, base_point):
        return (
            int(base_point[0] * self.scale_x),
            int(base_point[1] * self.scale_y),
        )