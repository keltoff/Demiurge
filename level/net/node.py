from local_types import Position
import pygame.draw
from pygame import Color, Rect
from ast import literal_eval as make_tuple


class Node:
    def __init__(self):
        self.pos = Position(0, 0)
        self.name = None
        self.links = dict()
        self.type = None

    def draw(self, surface, camera):
        rect = Rect(-40, -40, 20, 20)
        rect = camera.transform(rect.move(self.pos.x, self.pos.y))
        pygame.draw.rect(surface, pygame.Color('darkgray'), rect)
        pt = camera.transform(self.pos)
        pt = Position(pt[0], pt[1])
        pygame.draw.line(surface, pygame.Color('red'), pt.t, (pt + Position(-5, 0)).t)
        pygame.draw.line(surface, pygame.Color('red'), pt.t, (pt + Position(5, 0)).t)
        pygame.draw.line(surface, pygame.Color('red'), pt.t, (pt + Position(0, 5)).t)
        pygame.draw.line(surface, pygame.Color('red'), pt.t, (pt + Position(0, -5)).t)

    def join(self, direction, link):
        self.links[direction] = link

    @staticmethod
    def from_xml(xml_node):
        def load_tuple(val): return make_tuple(xml_node.attrib[val])

        position = load_tuple('pos')

        node = Node()
        node.pos = Position(position[0], position[1])
        node.name = xml_node.attrib['id']
        node.type = xml_node.attrib.get('type', 'junction')
        return node
