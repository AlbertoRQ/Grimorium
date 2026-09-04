from game import config

def apply_potion(player, potion_id):
    potion_data = config.POTION_DATA[potion_id]
    stat = potion_data["stat"]
    amount = potion_data["amount"]

    if stat == "health":
        player.health = min(player.max_health, player.health + amount)
        return

    current_value = getattr(player, stat)
    setattr(player, stat, current_value + amount)


def apply_book(player, book_id):
    player.books_purchased += 1
    player.purchased_books.add(book_id)

    effect = config.BOOK_DATA[book_id]["effect"]

    if "combo" in effect:
        combo = effect["combo"]

        for stat, bonus in effect.items():
            if stat != "combo":
                player.combo_stats[combo][stat] += bonus
        return

    element = effect["element"]

    for stat, bonus in effect.items():
        if stat != "element":
            player.element_stats[element][stat] += bonus


def apply_power(player, power_id):
    power_data = config.POWER_DATA[power_id]
    category = power_data.get("category", "element")

    if category == "shot_modifier":
        player.shot_modifiers.add(power_id)
        return

    element = power_data["element"]

    if element not in player.power_element_order:
        player.power_element_order.append(element)

    if power_data["mode"] == "base":
        if element not in player.base_bullet_elements:
            player.base_bullet_elements.append(element)
    else:
        player.extra_bullet_element[element] = power_data["chance"]