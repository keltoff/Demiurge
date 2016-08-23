from local_types import Pt
import pygame.draw
from pygame import Color, Rect
from ast import literal_eval as make_tuple
import helper


class Node:
    def __init__(self):
        self.pos = Pt(0, 0)
        self.name = None
        self.links = dict()
        self.type = None

    def draw(self, surface, camera):
        rect = Rect(camera.transform(self.pos), (0, 0)).inflate(20, 20)
        pygame.draw.rect(surface, Color('darkgray'), rect)
        pygame.draw.rect(surface, Color('black'), rect.inflate(-4, -4))
        # helper.marker(camera.transform(self.pos), surface)

    def join(self, direction, link):
        self.links[direction] = link

    @staticmethod
    def from_xml(xml_node):
        def load_tuple(val): return make_tuple(xml_node.attrib[val])

        position = load_tuple('pos')

        node = Node()
        node.pos = Pt(position)
        node.name = xml_node.attrib['id']
        node.type = xml_node.attrib.get('type', 'junction')
        return node
