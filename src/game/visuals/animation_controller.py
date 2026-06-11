class AnimationController:
    def __init__(self, animations, initial_state="idle", initial_facing="down"):
        self.animations = animations
        self.state = initial_state
        self.facing = initial_facing

        self.frame_index = 0
        self.timer = 0.0
        self.finished = False

    def _make_key(self):
        directional_key = f"{self.state}_{self.facing}"

        if directional_key in self.animations:
            return directional_key

        if self.state in self.animations:
            return self.state

        raise KeyError(f"Animation not found for state='{self.state}' facing='{self.facing}'")

    def get_current_animation(self):
        key = self._make_key()
        return self.animations[key]

    def set_state(self, state, reset=False):
        if state != self.state or reset:
            self.state = state
            self.frame_index = 0
            self.timer = 0.0
            self.finished = False

    def set_facing(self, facing):
        if facing != self.facing:
            self.facing = facing
            self.frame_index = 0
            self.timer = 0.0

    def update(self, dt):
        anim = self.get_current_animation()
        frames = anim["frames"]

        if len(frames) <= 1:
            return

        self.timer += dt

        if self.timer >= anim["speed"]:
            self.timer = 0.0
            self.frame_index += 1

            if self.frame_index >= len(frames):
                if anim.get("loop", True):
                    self.frame_index = 0
                else:
                    self.frame_index = len(frames) - 1
                    self.finished = True

    def get_frame_coords(self):
        anim = self.get_current_animation()
        row = anim["row"]
        frames = anim["frames"]
        col = frames[self.frame_index]
        return col, row