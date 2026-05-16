"""Control muy simple de oleadas."""


class WaveManager:
    def __init__(self):
        self.current_wave = 1
        self.time_in_wave = 0.0
        self.wave_duration = 20.0

    def update(self, dt):
        """Cada cierto tiempo sube la oleada."""
        self.time_in_wave += dt

        if self.time_in_wave >= self.wave_duration:
            self.time_in_wave = 0.0
            self.current_wave += 1
