"""Configuracion global del juego.

Es la misma idea que ya tenias en `estructura_simple/ajustes.py`,
pero puesta dentro de la estructura por carpetas.
"""

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 240
WINDOW_TITLE = "Grimorium"

ROOM_CELL_SIZE = 70
WALL_THICKNESS = 20

BACKGROUND_COLOR = (30, 30, 40)
PLAYER_COLOR = (80, 220, 120)
PLAYER_COLOR_INVENCIBLE = (160, 255, 180)
BULLET_COLOR = (218, 245, 244)
ENEMY_COLOR = (220, 90, 90)
ENEMY_BULLET_COLOR = (220, 30, 30)
HUD_COLOR = (255, 255, 255)
BUTTON_COLOR = (60, 70, 85)
BUTTON_HOVER_COLOR = (85, 100, 120)

PLAYER_RADIUS = 30

PLAYER_SPEED = 400
PLAYER_MAX_HEALTH = 3
PLAYER_FIRE_COOLDOWN = 0.4
PLAYER_DAMAGE = 1
PLAYER_BODY_DAMAGE = 0
PLAYER_LUCK = 0
PLAYER_SHOOT_DISTANCE = 350
PLAYER_INVULNERABILITY_TIME = 1


FORWARD_BONUS = 120
SIDE_DRIFT = 140

BULLET_RADIUS = 8
BULLET_SPEED = 550
BULLET_DAMAGE = 1
BULLET_RATE = 1

ENEMY_RADIUS = 18
ENEMY_SPEED = 130
ENEMY_MAX_HEALTH = 3
ENEMY_SPAWN_INTERVAL = 2.0
ENEMY_DAMAGE = 1
ENEMY_BODY_DAMAGE = 1

SHOOTER_ENEMY_RADIUS = 18
SHOOTER_ENEMY_SPEED = 110
SHOOTER_ENEMY_BULLET_SPEED = 340
SHOOTER_ENEMY_FIRE_COOLDOWN = 3
SHOOTER_ENEMY_COLOR = (200, 50, 200)
SHOOTER_ENEMY_SHOOT_DISTANCE = 350

BOSS_MAX_HEALTH = 1000
BOSS_RADIUS = 60
BOSS_REGEN = 2
BOSS_DAMAGE = 1
BOSS_BODY_DAMAGE = 2

# Se quedan definidas para no romper nada si luego reutilizas
# archivos del esqueleto anterior.
SPREAD_BULLET_COUNT = 3
SPREAD_ANGLE_STEP = 12
PIERCING_BULLET_DAMAGE = 1
PIERCING_BULLET_PENETRATION = 3
TANK_ENEMY_RADIUS = 26
TANK_ENEMY_SPEED = 90
TANK_ENEMY_MAX_HEALTH = 3
SPAWN_INTERVAL = ENEMY_SPAWN_INTERVAL
FONT_SIZE = 28

WIDTH, HEIGHT = 800, 600


COLORS_LIST = {
    "blanco": (255, 255, 255),
    "negro": (0, 0, 0),
    "rojo": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255),
    "amarillo": (255, 255, 0),
    "gris": (128, 128, 128)
}


RUN_PATTERN = [
    "normal",
    "shop",
    "normal",
    "normal",
    "shop",
    "normal",
    "normal",
    "boss",
    "shop",
]


POTION_DATA = {
    "health": {
        "stat": "health",
        "amount": 1000,
        "price": 2,
    },
    "speed": {
        "stat": "speed",
        "amount": 25,
        "price": 2,
    },
    "damage": {
        "stat": "damage",
        "amount": 0.5,
        "price": 2,
    },
    "body_damage": {
        "stat": "body_damage",
        "amount": 0.5,
        "price": 2,
    },
    "speed_atack": {
        "stat": "fire_rate",
        "amount": -0.025,
        "price": 2,
    },
    "luck": {
        "stat": "luck",
        "amount": 1,
        "price": 2,
    },
    "shoot_distance": {
        "stat": "shoot_distance",
        "amount": 5,
        "price": 2,
    } 
}

POWER_DATA = {
    "fire": {
        "mode": "base",
        "element": "fire",
        "chance": 1.0,
        "price": 0,
    },
    "ice": {
        "mode": "extra",
        "element": "ice",
        "chance": 0.50,
        "price": 0,
    },
}


BOOK_DATA = {
    "fire": {
        "price": 1,
        "effect": {
            "element": "fire",
            "level": 1,
            "burn_damage": 0.2,
            "burn_duration": 1.0,
        },
    },
    "ice": {
        "price": 1,
        "effect": {
            "element": "ice",
            "level": 1,
            "slow_duration": 0.2,
            "slow_multiplier": -0.1,
            "ice_duration": 0.2,
        },
    },
    "electric": {
        "price": 6,
        "effect": {
            "element": "electric",
            "shock_damage": 1.0,
        },
    },
    "fire_electric": {
        "price": 9,
        "effect": {
            "element": "fire",
            "burn_damage": 0.3,
            "burn_duration": 1.0,
        },
    },
    "fire_ice": {
        "price": 9,
        "effect": {
            "element": "fire",
            "burn_damage": 0.2,
            "burn_duration": 1.5,
        },
    },
    "fire_potion": {
        "price": 8,
        "effect": {
            "element": "fire",
            "burn_damage": 0.2,
            "burn_duration": 1.0,
        },
    },
    "ice_electric": {
        "price": 9,
        "effect": {
            "element": "ice",
            "slow_duration": 1.0,
            "slow_multiplier": 0.1,
        },
    },
    "potion_electric": {
        "price": 8,
        "effect": {
            "element": "electric",
            "shock_damage": 1.5,
        },
    },
    "potion_ice": {
        "price": 8,
        "effect": {
            "element": "ice",
            "slow_duration": 1.2,
            "slow_multiplier": 0.1,
        },
    },
    "potion": {
        "price": 5,
        "effect": {
            "element": "fire",
            "burn_duration": 0.5,
        },
    },
}