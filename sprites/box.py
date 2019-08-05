from pygame import Rect
import pygame.draw
from local_types import Pt
from ast import literal_eval as make_tuple
import helper


class BodyFactory:
    def __init__(self, shape_library={}):
        self.library = shape_library

    @staticmethod
    def from_xml(model_nodes):

        rect_lib = dict()

        for model_node in model_nodes:
            name = model_node.attrib['type']
            w, h = make_tuple(model_node.attrib['size'])
            link = model_node.attrib['link']

            if link == '_':
                rect = Rect(-w/2, -h, w, h)
            elif link == '+':
                rect = Rect(-w/2, -h/2, w, h)
            elif link in ['t', 'T']:
                rect = Rect(-w/2, 0, w, h)
            else:
                # center link is default i guess?
                rect = Rect(-w/2, -h/2, w, h)

            rect_lib[name] = rect

        return BodyFactory(rect_lib)

    def parse(self, xml_node):
        position = make_tuple(xml_node.attrib['pos'])
        model = xml_node.attrib['type']
        id = xml_node.attrib['id']

        body = Body()
        body.pos = Pt(position)
        body.name = id
        body.scheme = model
        body.shape = self.library[model]

        return body


class Body:
    def __init__(self):
        self.pos = Pt(0, 0)
        self.shape = Rect(0, 0, 30, 50)

        self.scheme = None
        self.name = None

    @property
    def cpos(self):
        return self.pos

    def update(self, level, keys):
        pass

    def draw(self, surface, camera):
        tpos = camera.transform(self.cpos)
        rect = self.shape.move(tpos.x, tpos.y)

        pygame.draw.rect(surface, pygame.Color('skyblue'), rect)

        helper.marker(tpos, surface)
