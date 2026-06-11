from game.visuals.animation_controller import AnimationController
from game.visuals.sprite_visual import SpriteVisual


class AnimatedVisual:
    def __init__(
        self,
        image_folder,
        image_name,
        animations,
        frame_cols,
        frame_rows,
        scale_x,
        scale_y,
        colorkey=None,
        use_alpha=False,
        initial_state="idle",
        initial_facing="down",
    ):
        self.sprite = SpriteVisual(
            image_folder=image_folder,
            image_name=image_name,
            frame_cols=frame_cols,
            frame_rows=frame_rows,
            scale_x=scale_x,
            scale_y=scale_y,
            colorkey=colorkey,
            use_alpha=use_alpha,
        )

        self.animator = AnimationController(
            animations=animations,
            initial_state=initial_state,
            initial_facing=initial_facing,
        )

        self.locked = False
        self.fixed_frame = None

        self.refresh()

    def refresh(self):
        if self.fixed_frame is not None:
            col, row = self.fixed_frame
        else:
            col, row = self.animator.get_frame_coords()

        self.sprite.set_frame(col, row)

    def set_state(self, state, reset=False):
        self.animator.set_state(state, reset=reset)
        self.refresh()

    def set_facing(self, facing):
        self.animator.set_facing(facing)
        self.refresh()

    def update(self, dt):
        if self.locked:
            return

        if self.fixed_frame is not None:
            return

        self.animator.update(dt)
        self.refresh()

    def set_fixed_frame(self, col, row):
        self.fixed_frame = (col, row)
        self.refresh()

    def clear_fixed_frame(self):
        self.fixed_frame = None
        self.refresh()

    def set_locked(self, value):
        self.locked = value

    def set_size(self, scale_x, scale_y):
        self.sprite.set_size(scale_x, scale_y)
        self.refresh()

    def draw(self, surface, x, y):
        self.sprite.draw(surface, x, y)

    def get_surface(self):
        return self.sprite.get_surface()
    
    def set_tint(self, color):
        self.sprite.set_tint(color)

    def clear_tint(self):
        self.sprite.clear_tint()