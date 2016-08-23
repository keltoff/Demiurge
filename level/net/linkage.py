import pygame.draw
from pygame import Color

class Linkage:
    def __init__(self):
        self.ends = (None, None)

    @classmethod
    def from_xml(cls, xml, nodes):
        n1, dir1 = xml.attrib['from'].split(' ')
        n2, dir2 = xml.attrib['to'].split(' ')

        node1 = nodes[n1]
        node2 = nodes[n2]

        link = cls()
        link.ends = (node1, node2)

        node1.join(dir1, link)
        node2.join(dir2, link)
        return link

    def draw(self, surface, camera):
        pass


class Straight(Linkage):
    def draw(self, surface, camera):
        pygame.draw.line(surface, Color('gray'), camera.transform(self.ends[0].pos), camera.transform(self.ends[1].pos), 5)
        pygame.draw.line(surface, Color('black'), camera.transform(self.ends[0].pos), camera.transform(self.ends[1].pos), 3)
