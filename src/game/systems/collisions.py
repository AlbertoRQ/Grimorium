"""Funciones de colision.

Separarlas aqui te ayuda a no mezclar estas reglas
con el codigo de dibujo o de menus.
"""

import math
from game.systems.effect_handlers import ELEMENT_EFFECTS
from game.systems.element_combos import ELEMENTAL_COMBOS


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


def get_enemy_active_states(enemy):
    states = []

    if enemy.status_effects["burn"]["is_burned"]:
        states.append("burn")

    if enemy.status_effects["ice"]["is_ice"]:
        states.append("ice")

    return states


def try_apply_combo(bullet, enemy, element, hit_damage):
    active_states = get_enemy_active_states(enemy)

    for state in active_states:
        combo_handler = ELEMENTAL_COMBOS.get((element, state))
        if combo_handler is not None:
            combo_handler(bullet, enemy, hit_damage)
            return True

    return False

def resolve_player_bullets_vs_enemies(bullets, enemies, blockers, damage_multiplier=1):
    bullets_left = []
    enemies_left = enemies[:]
    points_gained = 0

    for bullet in bullets:
        bullet_hit = False
        damage = bullet.damage * damage_multiplier

        for enemy in enemies_left[:]:
            if circles_collide(bullet, enemy):
                enemy.take_damage(damage)

                knockback_strength = 250
                length = math.hypot(bullet.vel_x, bullet.vel_y)

                if length > 0:
                    enemy.apply_knockback(bullet.vel_x / length, bullet.vel_y / length, knockback_strength)

                for element in bullet.elements:
                    if try_apply_combo(bullet, enemy, element, damage):
                        continue

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