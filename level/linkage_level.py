from level.level_base import Level
from collections import namedtuple
import pygame.draw
from local_types import Pt
from sprites.box import BodyFactory, Body
from level.interactable import Interactable
import level.net as net


class Line:
    def __init__(self, color=(0, 180, 250)):
        self.color = color
        self.links = []

    def draw(self, surface, camera):
        pygame.draw.line(surface, self.color, camera.transform(self.end1), camera.transform(self.end2))

    @property
    def end1(self):
        return Pt(0, 0)

    @property
    def end2(self):
        return Pt(0, 0)


class HLine(Line):
    def __init__(self, y, x1, x2):
        Line.__init__(self)

        if x1 > x2:
            x1, x2 = x2, x1

        self.y = y
        self.x1 = x1
        self.x2 = x2

    @property
    def end1(self):
        return Pt(self.x1, self.y)

    @property
    def end2(self):
        return Pt(self.x2, self.y)

    def draw(self, surface, camera):
        Line.draw(self, surface, camera)

        l_color = (200, 0, 0)

        for l in self.links:
            l_pt = Pt(l.x, self.y)

            pygame.draw.line(surface, l_color, camera.transform(l_pt + (10, 10)), camera.transform(l_pt + (-10, 10)))
            pygame.draw.line(surface, l_color, camera.transform(l_pt + (10, -10)), camera.transform(l_pt + (-10, -10)))


class VLine(Line):
    def __init__(self, x, y1, y2):
        Line.__init__(self)

        if y1 > y2:
            y1, y2 = y2, y1

        self.x = x
        self.y1 = y1
        self.y2 = y2

    @property
    def end1(self):
        return Pt(self.x, self.y1)

    @property
    def end2(self):
        return Pt(self.x, self.y2)

    def draw(self, surface, camera):
        Line.draw(self, surface, camera)

        l_color = (200, 0, 0)

        for l in self.links:
            l_pt = Pt(self.x, l.y)

            pygame.draw.line(surface, l_color, camera.transform(l_pt + (10, -10)), camera.transform(l_pt + (10, 10)))
            pygame.draw.line(surface, l_color, camera.transform(l_pt + (-10, -10)), camera.transform(l_pt + (-10, 10)))


class Linkage(Level):
    def __init__(self):
        self.hlines = []
        self.vlines = []

        self.bodies = []

    def draw(self, surface, camera):
        # def draw_all(X):
        #     for x in X:
        #         x.draw(surface, camera)

        for l in self.hlines + self.vlines:
            l.draw(surface, camera)

        for b in self.bodies:
            b.draw(surface, camera)

    def load(self, xml):
        for h in xml.findall('walls/horizontal'):
            def out(val): return int(h.attrib[val])
            self.hlines.append(HLine(x1=out('x1'), x2=out('x2'), y=out('y')))

        for v in xml.findall('walls/vertical'):
            def out(val): return int(v.attrib[val])
            self.vlines.append(VLine(x=out('x'), y1=out('y1'), y2=out('y2')))

        for h in self.hlines:
            for v in self.vlines:
                if touch(h, v):
                    h.links.append(v)
                    v.links.append(h)

        factory = BodyFactory.from_xml(xml.findall('bodies/model'))

        self.bodies = [factory.parse(body_xml) for body_xml in xml.findall('bodies/body')]


def touch(h, v):
    return (v.y1 <= h.y <= v.y2) and (h.x1 <= v.x <= h.x2)
