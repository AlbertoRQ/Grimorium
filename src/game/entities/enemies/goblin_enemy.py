
from game.entities.enemies.shooter_enemy import ShooterEnemy
from game.visuals.animated_visual import AnimatedVisual



class GoblinEnemy(ShooterEnemy):
    def __init__(self, position, level=1):
        super().__init__(position, level)

        self.visual = AnimatedVisual(
                image_folder="enemies/goblin",
                image_name="goblin.png",
                frame_cols=1,
                frame_rows=1,
                scale_x=32,
                scale_y=32,
                use_alpha=False,
                colorkey=(84, 206, 76),
                initial_state="idle",
                initial_facing="down",
                animations={
                    "idle": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                    "walk": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                },
            )