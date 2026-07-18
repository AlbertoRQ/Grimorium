import random

import pygame

from game import config


DEFAULT_SHOT_CONTEXT = {
    "fan_count": 1,
    "fan_angle": 0,
    "parallel_count": 1,
    "parallel_spacing": 0,
    "radius_multiplier": 1.0,
    "damage_multiplier": 1.0,
    "speed_multiplier": 1.0,
    "range_multiplier": 1.0,
    "cooldown_multiplier": 1.0,

    "rear_shot": False,
}


DEFAULT_MODIFIER_OPERATIONS = {
    "fan_count": "set",
    "fan_angle": "set",
    "parallel_count": "set",
    "parallel_spacing": "set",
    "radius_multiplier": "multiply",
    "damage_multiplier": "multiply",
    "speed_multiplier": "multiply",
    "range_multiplier": "multiply",
    "cooldown_multiplier": "multiply",
    "rear_shot": "set",
}


BASE_TYPE_CONTEXTS = {
    "normal": {},
    "gatling": {},
    "spread": {
        "fan_count": 3,
        "fan_angle": 12,
    },
}


def build_player_shot(player, vel_x, vel_y):

    from game.entities.bullets.bullet import build_bullet

    bullet_type = getattr(player, "bullet_type", "normal")
    context = build_shot_context(player.shot_modifiers, bullet_type)

    angles = build_fan_angles(
        context["fan_count"],
        context["fan_angle"],
    )

    if context["rear_shot"]:
        forward_angles = angles.copy()

        rear_angles = [
            angle + 180
            for angle in forward_angles
        ]

        angles.extend(rear_angles)

    parallel_offsets = build_parallel_offsets(
        context["parallel_count"],
        context["parallel_spacing"],
    )

    base_velocity = pygame.Vector2(vel_x, vel_y)
    base_velocity *= context["speed_multiplier"]

    bullets = []

    for angle in angles:
        rotated_velocity = base_velocity.rotate(angle)

        if rotated_velocity.length_squared() <= 0:
            continue

        direction = rotated_velocity.normalize()
        perpendicular = pygame.Vector2(-direction.y, direction.x)

        for offset in parallel_offsets:
            spawn_position = (
                pygame.Vector2(player.x, player.y)
                + perpendicular * offset
            )

            # Cada proyectil hace sus propias tiradas elementales.
            elements = roll_bullet_elements(player)
            effect_data = build_bullet_effect_data(player, elements)

            bullet = build_bullet(
                spawn_position.x,
                spawn_position.y,
                rotated_velocity.x,
                rotated_velocity.y,
                player.shoot_distance * context["range_multiplier"],
                bullet_type,
                elements,
                effect_data,
                context["radius_multiplier"],
            )

            bullet.damage = player.damage * context["damage_multiplier"]
            bullets.append(bullet)

    if not bullets:
        return [], 1.0

    cooldown_multiplier = (
        bullets[0].rate
        * context["cooldown_multiplier"]
    )
    return bullets, cooldown_multiplier


def build_shot_context(modifier_ids, bullet_type="normal"):
    """Combina la configuración base y los modificadores adquiridos."""
    context = DEFAULT_SHOT_CONTEXT.copy()
    context.update(BASE_TYPE_CONTEXTS.get(bullet_type, {}))

    # POWER_DATA fija un orden determinista aunque modifier_ids sea un set.
    for modifier_id, power_data in config.POWER_DATA.items():
        if modifier_id not in modifier_ids:
            continue

        modifier_data = power_data.get("modifier", {})

        for field, configured_value in modifier_data.items():
            apply_modifier(context, field, configured_value)

    return context


def apply_modifier(context, field, configured_value):
    """Aplica valores simples actuales y operaciones configurables futuras."""
    if field not in context:
        raise ValueError(f"Modificador de disparo desconocido: {field}")

    if isinstance(configured_value, dict):
        operation = configured_value.get(
            "operation",
            DEFAULT_MODIFIER_OPERATIONS[field],
        )
        value = configured_value["value"]
    else:
        operation = DEFAULT_MODIFIER_OPERATIONS[field]
        value = configured_value

    if operation == "set":
        context[field] = value
    elif operation == "add":
        context[field] += value
    elif operation == "multiply":
        context[field] *= value
    else:
        raise ValueError(
            f"Operación de modificador desconocida: {operation}"
        )


def build_fan_angles(count, angle_step):
    count = max(1, int(count))
    middle = (count - 1) / 2
    return [
        (index - middle) * angle_step
        for index in range(count)
    ]


def build_parallel_offsets(count, spacing):
    count = max(1, int(count))
    middle = (count - 1) / 2
    return [
        (index - middle) * spacing
        for index in range(count)
    ]


def roll_bullet_elements(player):
    elements = player.base_bullet_elements.copy()

    for element, chance in player.extra_bullet_element.items():
        if random.random() < chance:
            elements.append(element)

    return elements


def build_bullet_effect_data(player, elements):
    effect_data = {
        "combos": {
            combo_id: combo_data.copy()
            for combo_id, combo_data in player.combo_stats.items()
        }
    }

    for element in elements:
        if element in player.element_stats:
            effect_data[element] = player.element_stats[element].copy()

    return effect_data
