from local_types import Pt
from pygame import Rect


class Camera:
    def __init__(self, screen_center):
        self.pos = Pt(0, 0)
        self.scale = Pt(1.0, -1.0)
        self.screen_center = screen_center
        self.target = self.pos

    def transform(self, X):
        if isinstance(X, Pt):
            return self.screen_center + (X - self.pos) * self.scale
        if isinstance(X, Rect):
            center = Pt(X.center)
            size = Pt(X.size) * self.scale
            pos = self.screen_center + (center - self.pos) * self.scale
            return Rect((pos + (size*0.5)), size)

    def focus_on(self, target):
        self.target = target
        self.update()

    def update(self):
        if isinstance(self.target, Pt):
            self.pos = self.target
        elif isinstance(self.target, tuple):
            self.pos = Pt(self.target)
        elif hasattr(self.target, 'pos'):
            self.pos = self.target.pos
