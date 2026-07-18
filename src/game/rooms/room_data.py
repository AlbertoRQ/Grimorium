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
D = primera mitad de puerta doble / siguiente nivel en pared
d = segunda mitad de puerta doble
"""


BOSS_ROOM_1 = [
    "             ",
    "          Dd ",
    ".............",
    "......B......",
    ".............",
    ".............",
    ".............",
    ".............",
    "..........P..",
    "         Aa  ",
]

BOSS_ROOM_2 = [
    "             ",
    "          Dd ",
    ".............",
    ".OOO..B..OOO.",
    ".............",
    ".OOO.....OOO.",
    ".............",
    "..........P..",
    "         Aa  ",
]

RANDOM_ROOM_1 = [
    "             ",
    "          Dd ",
    ".............",
    "..E...E...E..",
    ".............",
    ".....OOO.....",
    ".....OOO.....",
    ".............",
    ".............",
    "..........P..",
    "         Aa  ",
]

RANDOM_ROOM_2 = [
    "             ",
    "          Dd ",
    "OO..........O",
    "..E...E...E..",
    "....E...E....",
    "VVVV.....VVVV",
    ".............",
    ".............",
    "OO.........OO",
    "..........P..",
    "         Aa  ",
]

RANDOM_ROOM_L = [
    "             ",
    "          Dd ",
    ".............",
    ".E..E........",
    ".....E...    ",
    "E......E.    ",
    ".........    ",
    ".............",
    ".............",
    "..........P..",
    "         Aa  ",
]

RANDOM_ROOM_O = [
    "             ",
    "          Dd ",
    ".....E.......",
    ".E....E......",
    "...       ...",
    "...       .E.",
    "...       ...",
    "...       ...",
    ".............",
    "..E.......P..",
    "         Aa  ",
]


RANDOM_ROOM_S = [
    "             ",
    "          Dd ",
    ".............",
    ".           .",
    ".           .",
    ".............",
    "            .",
    "            .",
    ".............",
    ".         .P.",
    "          Aa ",
]


RANDOM_ROOM_BOX = [
    "             ",
    "..E.E..E..E..",
    "             ",
    "EEEEEEEEEEEEE",
    "VVVVVVVVVVVVV",
    ".....E.......",
    ".E...........",
    ".............",
    "..........P..",
    "  Dd     Aa  ",
]


RANDOM_ROOM_ZAP = [
    "     Dd      ",
    "EVVV....VVVE",
    "VVvV....VEVV",
    "VVVV....VVVE",
    "VVEV....VEVV",
    "VVVV....VVVE",
    "VVvV....VEVV",
    "EVVV....VVVE",
    "VV......P.VV",
    "       Aa   ",
]

RANDOM_ROOM_CROSS = [
    "      Dd     ",
    "     ....    ",
    "     ....    ",
    "............",
    "............",
    "............",
    "............",
    "    ....    ",
    "    ..P.    ",
    "     Aa     ",
]


NORMAL_ROOMS = [
    RANDOM_ROOM_1,
    RANDOM_ROOM_2,
    RANDOM_ROOM_L,
    RANDOM_ROOM_O,
    RANDOM_ROOM_S,
    RANDOM_ROOM_BOX,
    RANDOM_ROOM_ZAP,
    RANDOM_ROOM_CROSS
]

BOSS_ROOMS = [
    BOSS_ROOM_1,
    BOSS_ROOM_2
]


def get_random_normal_room():
    return random.choice(NORMAL_ROOMS)

def get_random_boss_room():
    return random.choice(BOSS_ROOMS)
