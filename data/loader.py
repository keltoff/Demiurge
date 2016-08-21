from xml.etree import ElementTree as et


def load(filename='data/level1.xml'):
    data = et.parse(filename)
    return LevelFile(data)


class LevelFile:
    def __init__(self, tree):
        self.tree = tree

    @property
    def walls_h(self):
        for h in self.tree.find('walls/horizontal'):
            def out(val): return int(h.attrib[val])
            yield out('x1'), out('x2'), out('y')

    @property
    def walls_v(self):
        for v in self.tree.find('walls/vertical'):
            def out(val): return int(v.attrib[val])
            yield out('x'), out('y1'), out('y2')
