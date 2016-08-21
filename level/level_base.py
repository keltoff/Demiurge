from xml.etree import ElementTree as et


class Level:
    def draw(self, surface, camera):
        pass

    def can_move(self, pos, delta, w=1, h=1, constraint=None):
        return pos+delta, []

    def load(self, xml):
        pass

    @classmethod
    def from_xml(cls, filename='data/level1.xml'):
        l = cls()
        l.load(et.parse(filename))
        return l
