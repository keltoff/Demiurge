from pygame import Rect, Color
import pygame.draw
from local_types import Position
from ast import literal_eval as make_tuple


class Interactable:
    def __init__(self):
        self.pos = Position(0, 0)
        self.size = (30, 40)

        self.name = None
        self.action = None
        self.target = None

    @property
    def cpos(self):
        return self.pos

    @property
    def rect(self):
        return Rect(self.pos.x - self.size[0]/2, self.pos.y - self.size[1]/2, self.size[0], self.size[1])

    def update(self, level, keys):
        pass

    def draw(self, surface, camera):
        pygame.draw.rect(surface, pygame.Color('darkgreen'), camera.transform(self.rect))

    @staticmethod
    def from_xml(xml_node):
        def load_tuple(val): return make_tuple(xml_node.attrib[val])

        position = load_tuple('pos')

        obj = Interactable()
        obj.pos = Position(position[0], position[1])
        # obj.name = xml_node.attrib['id']
        obj.action = 'uplink'
        obj.target = xml_node.attrib['node']
        return obj
