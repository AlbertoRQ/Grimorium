import random

"""
# = pared
. = suelo
P = posición inicial del jugador
B = posición del jefe
E = enemigo normal
V = vacio
O = objeto
N = siguiente nivel
"""


BOSS_ROOM_1 = [
    ".............",
    "......B......",
    "......N......",
    ".............",
    "....I.I.I....",
    ".............",
    "......P......",
]

BOSS_ROOM_2 = [
    ".............",
    ".OOO..B..OOO.",
    "......N......",
    ".OOO.....OOO.",
    "....I.I.I....",
    ".............",
    "......P......",
]

RANDOM_ROOM_1 = [
    ".............",
    "..E...E...E..",
    "....I.I.I....",
    ".....OOO.....",
    ".N...OOO.....",
    ".............",
    "......P......",
]

RANDOM_ROOM_2 = [
    ".............",
    ".NE...E...E..",
    "....I.I.I....",
    "VVVVVV.VVVVVV",
    ".............",
    ".............",
    "OO....P....OO",
]

RANDOM_ROOM_L = [
    ".............",
    ".E..E......N.",
    ".............",
    ".......      ",
    ".......      ",
    ".I.I.I.......",
    "...........P.",
]


NORMAL_ROOMS = [
    RANDOM_ROOM_1,
    RANDOM_ROOM_2,
    RANDOM_ROOM_L
]

BOSS_ROOMS = [
    BOSS_ROOM_1,
    BOSS_ROOM_2
]


def get_random_normal_room():
    return random.choice(NORMAL_ROOMS)

def get_random_boss_room():
    return random.choice(BOSS_ROOMS)