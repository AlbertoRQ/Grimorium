"""Configuracion global del juego.

Es la misma idea que ya tenias en `estructura_simple/ajustes.py`,
pero puesta dentro de la estructura por carpetas.
"""

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Grimorium"

ROOM_CELL_SIZE = 70
WALL_THICKNESS = 20

BACKGROUND_COLOR = (30, 30, 40)
PLAYER_COLOR = (80, 220, 120)
PLAYER_COLOR_INVENCIBLE = (160, 255, 180)
ENEMY_COLOR = (220, 90, 90)
BULLET_COLOR = (255, 220, 90)
HUD_COLOR = (255, 255, 255)
BUTTON_COLOR = (60, 70, 85)
BUTTON_HOVER_COLOR = (85, 100, 120)

PLAYER_RADIUS = 30

PLAYER_SPEED = 600
PLAYER_MAX_HEALTH = 10000
PLAYER_FIRE_COOLDOWN = 0.5
PLAYER_DAMAGE = 1
PLAYER_BODY_DAMAGE = 0
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
SHOOTER_ENEMY_BULLET_SPEED = 450
SHOOTER_ENEMY_FIRE_COOLDOWN = 3
SHOOTER_ENEMY_COLOR = (200, 50, 200)

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


POTION_EFFECTS = {
    "health": ("max_health", 50),
    "speed": ("speed", 25),
    "damage": ("damage", 1),
    "body_damage": ("body_damage", 1),
    "speed_atack": ("fire_rate", -0.1),
}