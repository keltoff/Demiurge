__author__ = 'tryid_000'

class GUI:
    def __init__(self):
        self.components = []

    def draw(self, surface):
        for cmp in self.components:
            cmp.draw(surface)