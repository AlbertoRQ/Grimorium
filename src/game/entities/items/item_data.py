import random


def get_item_data(item_id):
    return ITEM_DEFINITIONS[item_id]


def get_available_item_ids(player):
    available = []

    for item_id, data in ITEM_DEFINITIONS.items():
        requirements = data.get("requires", [])

        has_requirements = True

        for required_item in requirements:
            if required_item not in player.items:
                has_requirements = False
                break

        if has_requirements:
            available.append(item_id)

    return available


def choose_random_item_id(player):
    item_ids = get_available_item_ids(player)

    weights = [
        ITEM_DEFINITIONS[item_id]["weight"]
        for item_id in item_ids
    ]

    return random.choices(item_ids, weights=weights, k=1)[0]


ITEM_DEFINITIONS = {
    # Disparo
    "normal_shot": {
        "name": "Disparo normal",
        "description": "Vuelve al disparo basico.",
        "category": "shot_type",
        "rarity": "common",
        "weight": 30,
        "color": (255, 220, 90),  # amarillo
        "effect": {
            "type": "set_shot",
            "value": "normal",
        },
    },

    "triple_shot": {
        "name": "Disparo triple",
        "description": "Dispara tres balas en abanico.",
        "category": "shot_type",
        "rarity": "uncommon",
        "weight": 18,
        "color": (200, 0, 255),  # morado
        "effect": {
            "type": "set_shot",
            "value": "spread",
        },
    },

    # Balas
    "fire_bullets": {
        "name": "Balas de fuego",
        "description": "Las balas aplican dano extra durante 2 ticks.",
        "category": "bullet_effect",
        "rarity": "uncommon",
        "weight": 14,
        "color": (255, 100, 30),  # naranja fuego
        "effect": {
            "type": "set_bullet_effect",
            "value": "fire",
            "ticks": 2,
        },
    },

    # Combos
    "fire_upgrade": {
        "name": "Mejora de fuego",
        "description": "Aumenta el dano del fuego si ya tienes balas de fuego.",
        "category": "combo",
        "rarity": "rare",
        "weight": 8,
        "color": (255, 50, 20),  # rojo fuego
        "requires": ["fire_bullets"],
        "effect": {
            "type": "upgrade_effect",
            "value": "fire",
            "extra_ticks": 1,
            "extra_damage": 1,
        },
    },

    # Mejoras stats
    "health_up": {
        "name": "Vida",
        "description": "Aumenta tu vida maxima.",
        "category": "stat",
        "rarity": "common",
        "weight": 25,
        "color": (80, 220, 120),  # verde
        "effect": {
            "type": "stat",
            "stat": "max_health",
            "amount": 50,
        },
    },

    "speed_up": {
        "name": "Movimiento",
        "description": "Aumenta tu velocidad de movimiento.",
        "category": "stat",
        "rarity": "common",
        "weight": 22,
        "color": (80, 180, 255),  # azul claro
        "effect": {
            "type": "stat",
            "stat": "speed",
            "amount": 200,
        },
    },

    "damage_up": {
        "name": "Dano",
        "description": "Aumenta el dano de tus balas.",
        "category": "stat",
        "rarity": "common",
        "weight": 22,
        "color": (240, 80, 80),  # rojo
        "effect": {
            "type": "stat",
            "stat": "damage",
            "amount": 1,
        },
    },

    "fire_rate_up": {
        "name": "Cadencia",
        "description": "Reduce el tiempo entre disparos.",
        "category": "stat",
        "rarity": "common",
        "weight": 18,
        "color": (255, 230, 80),  # amarillo claro
        "effect": {
            "type": "stat_multiplier",
            "stat": "fire_rate",
            "multiplier": 0.5,
        },
    },

    # Extra
    "flight": {
        "name": "Vuelo",
        "description": "Permite atravesar vacios.",
        "category": "extra",
        "rarity": "rare",
        "weight": 6,
        "color": (180, 240, 255),  # celeste
        "effect": {
            "type": "flag",
            "flag": "can_fly",
            "value": True,
        },
    },
}


RARITY_WEIGHTS = {
    "common": 100,
    "uncommon": 60,
    "rare": 25,
    "legendary": 8,
}
