
from game.entities.enemies.chaser_enemy import ChaserEnemy
from game.visuals.animated_visual import AnimatedVisual



class RatEnemy(ChaserEnemy):
    def __init__(self, position, level=1):
        super().__init__(position, level)

        self.path_align_margin = 20
        self.path_arrival_distance = 2

        self.visual = AnimatedVisual(
            image_folder="enemies/rat",
            image_name="rat_animated.png",
            frame_cols=4,
            frame_rows=4,
            scale_x = 32,
            scale_y = 32,
            use_alpha=True,
            initial_state="idle",
            initial_facing="down",
            animations={
                "idle_right": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                "walk_right": {"row": 0, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_left": {"row": 1, "frames": [0], "speed": 0.25, "loop": True},
                "walk_left": {"row": 1, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_down": {"row": 2, "frames": [0], "speed": 0.25, "loop": True},
                "walk_down": {"row": 2, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},

                "idle_up": {"row": 3, "frames": [0], "speed": 0.25, "loop": True},
                "walk_up": {"row": 3, "frames": [0, 1, 2, 3], "speed": 0.25, "loop": True},
            },
        )