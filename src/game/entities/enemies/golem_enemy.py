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

        self.speed_animation = 0.40

        # self.visual = AnimatedVisual(
        #     image_folder="enemies/golem",
        #     image_name="golem_animated.png",
        #     frame_cols=4,
        #     frame_rows=4,
        #     scale_x = 64,
        #     scale_y = 64,
        #     use_alpha=True,
        #     initial_state="idle",
        #     initial_facing="down",
        #     animations={
        #         "idle_right": {"row": 3, "frames": [0], "speed": self.speed_animation, "loop": True},
        #         "walk_right": {"row": 3, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},

        #         "idle_left": {"row": 2, "frames": [0], "speed": self.speed_animation, "loop": True},
        #         "walk_left": {"row": 2, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},

        #         "idle_down": {"row": 0, "frames": [0], "speed": self.speed_animation, "loop": True},
        #         "walk_down": {"row": 0, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},

        #         "idle_up": {"row": 1, "frames": [0], "speed": self.speed_animation, "loop": True},
        #         "walk_up": {"row": 1, "frames": [0, 1, 2, 3], "speed": self.speed_animation, "loop": True},
        #     },
        # )

        self.visual = AnimatedVisual(
                image_folder="enemies/golem",
                image_name="golem.bmp",
                frame_cols=1,
                frame_rows=1,
                scale_x=64,
                scale_y=64,
                use_alpha=False,
                colorkey=(84, 206, 76),
                initial_state="idle",
                initial_facing="down",
                animations={
                    "idle": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                    "walk": {"row": 0, "frames": [0], "speed": 0.25, "loop": True},
                },
            )