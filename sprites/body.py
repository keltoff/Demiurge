# import pygame.Sprite
from pygame import Rect
import pygame.draw
from local_types import Pt
from ast import literal_eval as make_tuple
import helper


# class Body(pygame.Sprite):
class Body():
    def __init__(self):
        self.pos = Pt(0, 0)
        # self.radius = Position(15, -25)
        self.shape = Rect(0, 0, 30, 50)

        self.scheme = None
        self.name = None

    @property
    def cpos(self):
        # return self.pos - self.radius
        return self.pos

    @property
    def rect(self):
        return self.shape.move(self.pos.x, self.pos.y)

    def update(self, level, keys):
        pass

    def draw(self, surface, camera):
        tpos = camera.transform(self.cpos)
        # sprite = self.sprites[self.state.name]
        # surface.blit(sprite, tpos)

        pt = camera.transform(self.pos)
        br = Rect(pt, (0, self.shape.height)).inflate(self.shape.width/2, 0).move(0, -self.shape.height)
        # pygame.draw.rect(surface, pygame.Color('azure'), camera.transform(self.rect))

        pygame.draw.rect(surface, pygame.Color('skyblue'), br)
        # helper.marker(pt, surface)

        # tp = camera.transform(self.pos)
        # pygame.draw.line(surface, (200, 0, 0), (tp[0], tp[1]-10), (tp[0], tp[1]+10))
        # pygame.draw.line(surface, (200, 0, 0), (tp[0]-10, tp[1]), (tp[0]+10, tp[1]))

    @staticmethod
    def from_xml(xml_node):
        def load_tuple(val): return make_tuple(xml_node.attrib[val])

        position = load_tuple('pos')
        size = load_tuple('size')
        scheme = xml_node.attrib['scheme']

        body = Body()
        body.pos = Pt(position)
        body.shape = Rect((0, 0), size)
        body.name = xml_node.attrib['id']
        # body.scheme = schemes.get(scheme)
        body.scheme = scheme
        return body
