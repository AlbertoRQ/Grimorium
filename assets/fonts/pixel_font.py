import pygame

FONT_PATH = "assets/fonts/3x5light.png"

CHAR_W = 3
CHAR_H = 5
COLS = 16
SCALE = 4

CHAR_SPACING_X = 1
CHAR_SPACING_Y = 1

CHAR_WIDTHS = {
    ".": 1,
    ",": 1,
    ":": 1,
    ";": 1,
    "!": 1,
    "i": 1,
    "l": 1,
}

# Orden típico ASCII: espacio, !, ", #, $, %, ..., A, B, C...
CHAR_ORDER = "".join(chr(i) for i in range(32, 128)) + "áéíóúÁÉÍÓÚñÑüÜ¿¡"


class PixelFont:
    def __init__(self, path, scale=4):
        self.sheet = pygame.image.load(path).convert_alpha()
        self.scale = scale
        self.glyphs = {}

        for i, char in enumerate(CHAR_ORDER):
            x = (i % COLS) * (CHAR_W + CHAR_SPACING_X)
            y = (i // COLS) * (CHAR_H + CHAR_SPACING_Y)

            rect = pygame.Rect(x, y, CHAR_W, CHAR_H)
            glyph = self.sheet.subsurface(rect).copy()

            glyph_width = CHAR_WIDTHS.get(char, CHAR_W)
            offset_x = (CHAR_W - glyph_width) // 2
            glyph = glyph.subsurface(pygame.Rect(offset_x, 0, glyph_width, CHAR_H)).copy()

            glyph = pygame.transform.scale(
                glyph,
                (glyph_width * scale, CHAR_H * scale)
            )

            self.glyphs[char] = glyph

    def draw(self, surface, text, x, y):
        start_x = x

        for char in text:
            if char == "\n":
                x = start_x
                y += (CHAR_H + 2) * self.scale
                continue

            glyph = self.glyphs.get(char, self.glyphs.get("?"))

            if glyph:
                surface.blit(glyph, (x, y))

            char_width = CHAR_WIDTHS.get(char, CHAR_W)
            x += (char_width + 1) * self.scale