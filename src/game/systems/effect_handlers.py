def apply_fire_effect(bullet, enemy):
    if enemy.status_effects["burn"]["is_burned"] == False:
        enemy.status_effects["burn"]["is_burned"] = True
        enemy.status_effects["burn"]["timer"] = bullet.effect_data["fire"]["burn_duration"]
        enemy.status_effects["burn"]["tick_timer"] = bullet.effect_data["fire"]["burn_tick_timer"]
        enemy.status_effects["burn"]["damage"] = bullet.effect_data["fire"]["burn_damage"]

def apply_ice_effect(bullet, enemy):
    enemy_status = enemy.status_effects["ice"]

    if enemy_status["ice_cooldown"] > 0 or enemy_status["is_ice"]:
        return

    enemy_status["stacks"] += 1

    if enemy_status["stacks"] >= bullet.effect_data["ice"]["max_ice_stacks"]:
        enemy_status["is_ice"] = True
        enemy_status["cooldown_value"] = bullet.effect_data["ice"]["ice_cooldown"]
        enemy_status["ice_timer"] = bullet.effect_data["ice"]["ice_duration"]
        enemy_status["is_slowed"] = False
        enemy_status["slow_timer"] = 0
        return

    enemy_status["is_slowed"] = True
    enemy_status["slow_timer"] = bullet.effect_data["ice"]["slow_duration"]
    enemy_status["multiplier"] = bullet.effect_data["ice"]["slow_multiplier"]


ELEMENT_EFFECTS = {
    "fire": apply_fire_effect,
    "ice": apply_ice_effect,
}