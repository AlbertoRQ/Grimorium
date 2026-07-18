from game import config
from game.entities.enemies.chaser_enemy import ChaserEnemy
from game.visuals.animated_visual import AnimatedVisual


class GolemEnemy(ChaserEnemy):
    def __init__(self, position, level=1):
        super().__init__(position, level)

        
        self.speed = config.ENEMY_SPEED * 0.65
        self.base_speed = self.speed
        self.radius = 13
        self.score_value = 20

        self.path_align_margin = 2
        self.path_arrival_distance = 10

        self.visual = AnimatedVisual(
            image_folder="enemies/golem",
            image_name="golem.bmp",
            frame_cols=1,
            frame_rows=1,
            scale_x=64,
            scale_y=64,
            colorkey=(84, 206, 76),
            use_alpha=False,
            initial_state="idle",
            initial_facing="down",
            animations={
                "idle": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                "walk": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
            },
        )