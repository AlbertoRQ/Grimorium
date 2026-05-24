"""Funciones de colision.

Separarlas aqui te ayuda a no mezclar estas reglas
con el codigo de dibujo o de menus.
"""

import math


def circles_collide(a, b):
    distance = math.hypot(a.x - b.x, a.y - b.y)
    return distance <= a.radius + b.radius

def separate_circles(a, b, blockers):
    dx = b.x - a.x
    dy = b.y - a.y
    distance = math.hypot(dx, dy)
    min_distance = a.radius + b.radius

    if distance == 0:
        dx = 1
        dy = 0
        distance = 1

    if distance >= min_distance:
        return

    overlap = min_distance - distance
    normal_x = dx / distance
    normal_y = dy / distance

    push_x = normal_x * (overlap / 2)
    push_y = normal_y * (overlap / 2)

    new_ax = a.x - push_x
    new_ay = a.y - push_y
    new_bx = b.x + push_x
    new_by = b.y + push_y

    old_ax, old_ay = a.x, a.y
    a.x, a.y = new_ax, new_ay

    if a.collides_with_rects(blockers):
        a.x, a.y = old_ax, old_ay

    old_bx, old_by = b.x, b.y
    b.x, b.y = new_bx, new_by

    if b.collides_with_rects(blockers):
        b.x, b.y = old_bx, old_by


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

def apply_electric_effect(bullet, enemy):
    enemy.take_damage(2)


ELEMENT_EFFECTS = {
    "fire": apply_fire_effect,
    "ice": apply_ice_effect,
    "electric": apply_electric_effect,
}

def resolve_player_bullets_vs_enemies(bullets, enemies, damage_multiplier=1):
    bullets_left = []
    enemies_left = enemies[:]
    points_gained = 0

    for bullet in bullets:
        bullet_hit = False
        damage = bullet.damage * damage_multiplier

        for enemy in enemies_left[:]:
            if circles_collide(bullet, enemy):
                enemy.take_damage(damage)

                for element in bullet.elements:
                    effect = ELEMENT_EFFECTS.get(element)
                    if effect is not None:
                        effect(bullet, enemy)

                bullet_hit = True

                if enemy.is_dead():
                    enemies_left.remove(enemy)
                    points_gained += 0

                break

        if not bullet_hit:
            bullets_left.append(bullet)

    return bullets_left, enemies_left, points_gained


def resolve_enemy_bullets_vs_player(enemy_bullets, player):
    bullets_left = []

    for bullet in enemy_bullets:
        if circles_collide(bullet, player):
            player.take_damage(bullet.damage)
        else:
            bullets_left.append(bullet)

    return bullets_left


def resolve_enemies_touch_player(enemies, player, blockers):
    enemies_left = []
    points = 0

    for enemy in enemies:
        if circles_collide(enemy, player):
            player.take_damage(enemy.body_damage)

            if enemy.damage > 0:
                enemy.take_damage(player.body_damage)

            separate_circles(player, enemy, blockers)

            if not enemy.is_dead():
                enemies_left.append(enemy)
            else:
                points += 0
        
        else:
            enemies_left.append(enemy)
            

    return enemies_left, points