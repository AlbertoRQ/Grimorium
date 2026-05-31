"""HUD del juego."""

from game import config
from game.ui.fonts import create_font


class HUD:
    def __init__(self):
        self.font = create_font(config.FONT_SIZE)

    def draw(self, surface, player, score, wave_number):
        lines = [
            f"Vida: {int(player.health)}/{int(player.max_health)}",
            f"Puntos: {score}",
            f"Arma: {player.weapon_name}",
            f"Oleada: {wave_number}",
            "Q: cambiar arma | Click: disparar | ESC: pausa",
        ]

        y = 15
        for line in lines:
            text_surface = self.font.render(line, True, config.HUD_COLOR)
            surface.blit(text_surface, (15, y))
            y += 28
