import math
from game.systems.electric_chain import ElectricChain
from game.systems.ice_puddle import IcePuddle


def apply_fire_effect(bullet, enemy, _enemies, _hit_damage):
    if enemy.status_effects["burn"]["is_burned"] == False:
        enemy.status_effects["burn"]["is_burned"] = True
        enemy.status_effects["burn"]["timer"] = bullet.effect_data["fire"]["burn_duration"]
        enemy.status_effects["burn"]["tick_timer"] = bullet.effect_data["fire"]["burn_tick_timer"]
        enemy.status_effects["burn"]["damage"] = bullet.effect_data["fire"]["burn_damage"]

def apply_ice_effect(bullet, enemy, _enemies, _hit_damage):
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

        fragile = enemy.status_effects["fragile"]
        fragile["timer"] = bullet.effect_data["combos"]["ice_poison"]["fragile_duration"]
        
        combo_data = bullet.effect_data["combos"]["ice_electric"]

        puddle_duration = (
            bullet.effect_data["ice"]["ice_duration"]
            + combo_data["puddle_duration_bonus"]
        )

        return IcePuddle(
            enemy.x,
            enemy.y + enemy.radius * 0.45,
            enemy.radius,
            puddle_duration,
            combo_data,
        )

    enemy_status["is_slowed"] = True
    enemy_status["slow_timer"] = bullet.effect_data["ice"]["slow_duration"]
    enemy_status["multiplier"] = bullet.effect_data["ice"]["slow_multiplier"]


def apply_electric_effect(bullet, enemy, _enemies, hit_damage):
    electric_data = bullet.effect_data["electric"]

    damage = hit_damage * electric_data["damage_percentage"]
    max_jumps = electric_data["max_targets"]
    max_jump_distance = electric_data["max_jump_distance"]

    return ElectricChain(
        source=enemy,
        damage=damage,
        max_jumps=max_jumps,
        max_jump_distance=max_jump_distance,
    )


def apply_poison_effect(bullet, enemy, _enemies, _hit_damage):
    poison_data = bullet.effect_data["poison"]
    poison = enemy.status_effects["poison"]

    poison["max_stacks"] = poison_data["max_stacks"]
    poison["damage_taken_per_stack"] = poison_data["damage_taken_per_stack"]
    poison["stacks"] = min(poison["stacks"] + 1, poison["max_stacks"])

    try_execute_fragile_enemy(bullet, enemy)

    if getattr(enemy, "is_boss", False):
        poison["timer"] = poison_data["boss_duration"]


def try_execute_fragile_enemy(bullet, enemy):
    fragile = enemy.status_effects["fragile"]

    if fragile["timer"] <= 0:
        return

    poison = enemy.status_effects["poison"]
    combo_data = bullet.effect_data["combos"]["ice_poison"]

    stacks = poison["stacks"]

    if stacks <= 0:
        return

    execute_threshold = (
        combo_data["execute_base_threshold"]
        + stacks * combo_data["execute_threshold_per_stack"]
    )

    health_ratio = enemy.health / enemy.max_health

    if health_ratio <= execute_threshold:
        enemy.health = 0
        enemy.damage_flash_timer = 0.15


ELEMENT_EFFECTS = {
    "fire": apply_fire_effect,
    "ice": apply_ice_effect,
    "electric": apply_electric_effect,
    "poison": apply_poison_effect,
}