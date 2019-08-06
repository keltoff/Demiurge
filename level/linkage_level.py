from level.level_base import Level
from linkage_lines import HLine, VLine
import pygame.draw
from local_types import Pt
from sprites.box import BodyFactory


class Linkage(Level):
    def __init__(self):
        self.hlines = []
        self.vlines = []

        self.bodies = []

    def draw(self, surface, camera, focus):
        # def draw_all(X):
        #     for x in X:
        #         x.draw(surface, camera)

        for l in self.hlines + self.vlines:
            l.draw(surface, camera)

        for b in self.bodies:
            b.draw(surface, camera, b == focus)

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
        for b in self.bodies:
            for l in self.hlines + self.vlines:
                if is_on(b, l):
                    b.on_line = l
                    break


def touch(h, v):
    return (v.y1 <= h.y <= v.y2) and (h.x1 <= v.x <= h.x2)


def is_on(b, l):
    return (l.end1.y <= b.pos.y <= l.end2.y) and (l.end1.x <= b.pos.x <= l.end2.x)