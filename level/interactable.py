from pygame import Rect, Color
import pygame.draw
from local_types import Pt
from ast import literal_eval as make_tuple
import helper


class Interactable:
    def __init__(self):
        self.pos = Pt(0, 0)
        self.size = Pt(80, 100)

        self.name = None
        self.action = None
        self.target = None

    @property
    def rect(self):
        return Rect(self.pos, (0, self.size[1])).inflate(self.size[0]/2, 0).move(0, -self.size[1])
        # return Rect(self.pos, (0, 0)).inflate(*self.size/2)

    def update(self, level, keys):
        pass

    def draw(self, surface, camera):
        pt = camera.transform(self.pos)
        br = Rect(pt, (0, self.size[1])).inflate(self.size[0]/2, 0).move(0, -self.size[1])
        pygame.draw.rect(surface, Color('darkgreen'), br)
        # helper.marker(camera.transform(self.pos), surface)

    @staticmethod
    def from_xml(xml_node):
        def load_tuple(val): return make_tuple(xml_node.attrib[val])

        position = load_tuple('pos')

        obj = Interactable()
        obj.pos = Pt(position)
        # obj.name = xml_node.attrib['id']
        obj.action = 'uplink'
        obj.target = xml_node.attrib['node']
        return obj
