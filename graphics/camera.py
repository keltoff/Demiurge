__author__ = 'tryid_000'

from local_types import Position

class camera():
    def __init__(self, screen_center):
        self.pos = Position(0, 0)
        self.scale = Position(1.0, -1.0)
        self.screen_center = screen_center
        self.target = self.pos

    def transform(self, position):
        pos = self.screen_center + (position - self.pos) * self.scale
        return pos.x, pos.y

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
