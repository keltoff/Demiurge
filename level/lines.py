from level.level_base import Level
from collections import namedtuple
import pygame.draw
from local_types import Position
from sprites.body import Body
from level.interactable import Interactable
import level.net as net


HLine = namedtuple('HLine', 'x1 x2 y')
VLine = namedtuple('VLine', 'x y1 y2')


class Lines(Level):
    def __init__(self):
        self.hlines = []
        self.vlines = []
        self.bodies = []
        self.objects = []
        self.net = None
        self.G = Position(0, -5)

    def draw(self, surface, camera):
        def draw_all(X):
            for x in X:
                x.draw(surface, camera)

        color = (0, 180, 250)

        for l in self.hlines + self.vlines:
            pygame.draw.line(surface, color, camera.transform(_end1(l)), camera.transform(_end2(l)))

        draw_all(self.objects)
        draw_all(self.bodies)
        net.draw(self.net, surface, camera)

    def can_move(self, pos, delta, w=1, h=1, constraint=None):

        np = pos + delta
        hit = []

        for l, y in [(l, l.y) for l in self.hlines if l.x1 < pos.x < l.x2]:
            if np.y <= y+h <= pos.y:
                hit.append(('hit_D', l))
                np.y = y+h
            
            if pos.y <= y-h <= np.y:
                hit.append(('hit_U', l))
                np.y = y-h

        for l, x in [(l, l.x) for l in self.vlines if l.y1 < pos.y < l.y2]:
            if np.x <= x+w <= pos.x:
                hit.append(('hit_L', l))
                np.x = x+w
            
            if pos.x <= x-w <= np.x:
                hit.append(('hit_R', l))
                np.x = x-w

        if isinstance(constraint, HLine):
            if np.x < constraint.x1:
                hit.append(('drop', constraint.x1))
            if np.x > constraint.x2:
                hit.append(('drop', constraint.x2))
        if isinstance(constraint, VLine):
            if np.y < constraint.y1:
                hit.append(('drop', constraint.y1))
            if np.y > constraint.y2:
                hit.append(('drop', constraint.y2))

        return np, hit

    def load(self, xml):
        for h in xml.findall('walls/horizontal'):
            def out(val): return int(h.attrib[val])
            self.hlines.append(HLine(out('x1'), out('x2'), out('y')))
        for v in xml.findall('walls/vertical'):
            def out(val): return int(v.attrib[val])
            self.vlines.append(VLine(out('x'), out('y1'), out('y2')))

        self.objects = [Interactable.from_xml(t) for t in xml.findall('objects/terminal')]

        self.bodies = [Body.from_xml(b) for b in xml.findall('bodies/body')]

        self.net = net.from_xml(xml.find('net'))


def drawline(surface, color, camera, line):
    pygame.draw.line(surface, color, camera.transform(_end1(line)), camera.transform(_end2(line)))


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