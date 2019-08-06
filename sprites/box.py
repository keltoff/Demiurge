from pygame import Rect
import pygame.draw
from local_types import Pt
from ast import literal_eval as make_tuple
import helper
from level.linkage_lines import HLine, VLine


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
        
        self.speed = 10

        self.on_line = None

    @property
    def cpos(self):
        return self.pos

    def update(self, level, keys, is_player):
        if is_player:
            shift = Pt(0, 0)
            for key, change in {'UP': (0, 10), 'DN': (0, -10), 'LT': (-10, 0), 'RT': (10, 0)}.iteritems():
                if key in keys:
                    shift += change
            self.pos = self.on_line.try_move(self.pos + shift)

            switch, dist = None, float('inf')
            if isinstance(self.on_line, HLine):
                if 'UP' in keys:
                    switch, dist = self.on_line.up_closest(self.pos)
                if 'DN' in keys:
                    switch, dist = self.on_line.down_closest(self.pos)
            if isinstance(self.on_line, VLine):
                if 'LT' in keys:
                    switch, dist = self.on_line.left_closest(self.pos)
                if 'RT' in keys:
                    switch, dist = self.on_line.right_closest(self.pos)

            if switch and dist <= self.speed:
                self.on_line = switch
                self.pos = switch.try_move(self.pos)
        else:
            # AI
            pass

    def draw(self, surface, camera, is_player):
        tpos = camera.transform(self.cpos)
        rect = self.shape.move(tpos.x, tpos.y)

        if is_player:
            color = pygame.Color('blue')
        else:
            color = pygame.Color('gray')
        pygame.draw.rect(surface, color, rect)

        if self.on_line:
            helper.marker(tpos, surface, 'o')
        else:
            helper.marker(tpos, surface, 'x')
