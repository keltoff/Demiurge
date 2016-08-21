from local_types import Position
from pygame import Rect


class camera():
    def __init__(self, screen_center):
        self.pos = Position(0, 0)
        self.scale = Position(1.0, -1.0)
        self.screen_center = screen_center
        self.target = self.pos

    def transform(self, X):
        if isinstance(X, Position):
            pos = self.screen_center + (X - self.pos) * self.scale
            return pos.x, pos.y
        if isinstance(X, Rect):
            center = Position(X.center[0], X.center[1])
            size = Position(X.size[0], X.size[1]) * self.scale
            pos = self.screen_center + (center - self.pos) * self.scale
            return Rect((pos + (size*0.5)).t, size.t)

    def focus_on(self, target):
        self.target = target
        self.update()

    def update(self):
        if isinstance(self.target, tuple):
            self.pos = Position(self.target)
        if isinstance(self.target, Position):
            self.pos = self.target
        if hasattr(self.target, 'pos'):
            self.pos = self.target.pos
