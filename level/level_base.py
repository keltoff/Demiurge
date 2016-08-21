import math


class level:
    def draw(self, surface, camera):
        pass

    def canMove(self, pos, delta, w=1, h=1, constraint=None):
        return pos+delta, []