from level.level_base import level

__author__ = 'tryid_000'

from collections import namedtuple
import pygame.draw
from local_types import Position


HLine = namedtuple('HLine', 'x1 x2 y')
VLine = namedtuple('VLine', 'x y1 y2')

class lines(level):
    def __init__(self):
        self.hlines = []
        self.vlines = []
        self.G = Position(0, -5)

    def draw(self, surface, camera):
        color = (0, 180, 250)
        for l in self.hlines + self.vlines:
            pygame.draw.line(surface, color, camera.transform(_end1(l)), camera.transform(_end2(l)))

    def canMove(self, pos, delta, w=1, h=1):

        np = pos + delta
        hit = []

        for y in [l.y for l in self.hlines if l.x1 < pos.x < l.x2]:
            if np.y <= y+h <= pos.y:
                hit.append('hit_D')
                np.y = y+h
            
            if pos.y <= y-h <= np.y:
                hit.append('hit_U')
                np.y = y-h
            
                
        for x in [l.x for l in self.vlines if l.y1 < pos.y < l.y2]:
            if np.x <= x+w <= pos.x:
                hit.append('hit_L')
                np.x = x+w
            
            if pos.x <= x-w <= np.x:
                hit.append('hit_R')
                np.x = x-w
                
        return np, hit

    def add_h_line(self, x1, x2, y):
        self.hlines.append(HLine(x1, x2, y))

    def add_v_line(self, x, y1, y2):
        self.vlines.append(VLine(x, y1, y2))


def _end1(line):
    if isinstance(line, HLine):
        return Position(line.x1, line.y)
    if isinstance(line, VLine):
        return Position(line.x, line.y1)

def _end2(line):
    if isinstance(line, HLine):
        return Position(line.x2, line.y)
    if isinstance(line, VLine):
        return Position(line.x, line.y2)
    
    # 
    # def canMove(self, pos):
    #     limit = level.canMove(self, pos)
    #     for y in [l.y for l in self.hlines if l.x1 < pos.x < l.x2]:
    #         if y >= pos.y:
    #             limit['UP'] = min(limit['UP'], y)
    #         if y <= pos.y:
    #             limit['DOWN'] = max(limit['DOWN'], y)
    #     for x in [l.x for l in self.vlines if l.y1 < pos.y < l.y2]:
    #         if x <= pos.x:
    #             limit['LEFT'] = max(limit['LEFT'], x)
    #         if x >= pos.x:
    #             limit['RIGHT'] = min(limit['RIGHT'], x)
    #     return limit