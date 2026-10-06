import math

class Target:
    def __init__(self, x, y, base_radius=40, min_radius=12, lifespan_frames=90):
        self.x = x
        self.y = y
        self.base_radius = base_radius
        self.min_radius = min_radius
        self.lifespan_frames = lifespan_frames
        self.age = 0

    def update(self):
        self.age += 1

    def expired(self):
        return self.age >= self.lifespan_frames

    def visual_radius(self):
        # The target shrinks as it ages, giving the player less time
        # to react the longer it's been on screen.
        t = min(1.0, self.age / self.lifespan_frames)
        return self.base_radius - (self.base_radius - self.min_radius) * t

    def contains_point(self, x, y):
        # TASK 1 FIX: Hit-testing now uses visual_radius() so the clickable
        # area always matches exactly what is drawn on screen. Previously
        # base_radius was used, which never shrank, meaning a click well
        # outside the small visible circle could still register as a hit.
        return math.hypot(self.x - x, self.y - y) <= self.visual_radius()
