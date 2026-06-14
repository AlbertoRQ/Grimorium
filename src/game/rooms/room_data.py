import random

"""
# = pared
. = suelo
P = posición inicial del jugador
B = posición del jefe
E = enemigo normal
V = vacio
O = objeto
I = item
N = siguiente nivel
"""


BOSS_ROOM_1 = [
    "             ",
    ".............",
    "......B......",
    "......N......",
    ".............",
    ".............",
    ".............",
    "......P......",
]

BOSS_ROOM_2 = [
    "             ",
    ".............",
    ".OOO..B..OOO.",
    "......N......",
    ".OOO.....OOO.",
    ".............",
    ".............",
    "......P......",
]

RANDOM_ROOM_1 = [
    "             ",
    ".............",
    "..E...E...E..",
    ".............",
    ".....OOO.....",
    ".N...OOO.....",
    ".............",
    "......P......",
    ".............",
]

RANDOM_ROOM_2 = [
    "             ",
    "OO..........O",
    ".NE...E...E..",
    ".............",
    "VVVV.....VVVV",
    ".............",
    ".............",
    "OO....P....OO",
    ".............",
]

RANDOM_ROOM_L = [
    "             ",
    "...........N.",
    ".E..E........",
    ".........    ",
    ".........    ",
    ".........    ",
    ".............",
    "...........P.",
    ".............",
]

RANDOM_ROOM_O = [
    "             ",
    "...........N.",
    ".E...........",
    "...       ...",
    "...       ...",
    "...       ...",
    "...       ...",
    "...........P.",
    ".............",
]


RANDOM_ROOM_S = [
    "             ",
    "...........N.",
    ".           .",
    ".           .",
    ".............",
    "            .",
    "            .",
    ".............",
    ".           P",
]


NORMAL_ROOMS = [
    RANDOM_ROOM_1,
    RANDOM_ROOM_2,
    RANDOM_ROOM_L,
    RANDOM_ROOM_O,
    RANDOM_ROOM_S,
]

BOSS_ROOMS = [
    BOSS_ROOM_1,
    BOSS_ROOM_2
]


def get_random_normal_room():
    return random.choice(NORMAL_ROOMS)

def get_random_boss_room():
    return random.choice(BOSS_ROOMS)