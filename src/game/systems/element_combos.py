def apply_fire_on_ice_combo(bullet, enemy, hit_damage):
    ice = enemy.status_effects["ice"]

    ice["is_ice"] = False
    ice["ice_timer"] = 0
    ice["is_slowed"] = False
    ice["slow_timer"] = 0
    ice["stacks"] = 0
    ice["ice_cooldown"] = ice["cooldown_value"]

    enemy.speed = enemy.base_speed
    enemy.color = enemy.base_color

    multiplier = bullet.effect_data["combos"]["fire_ice"]["damage_multiplier"]
    enemy.take_damage(hit_damage * multiplier)

ELEMENTAL_COMBOS = {
    ("fire", "ice"): apply_fire_on_ice_combo,
}