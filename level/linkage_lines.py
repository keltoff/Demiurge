import pygame.draw
from local_types import Pt


max_dist = float('inf')


class Line:
    def __init__(self, color=(0, 180, 250)):
        self.color = color
        self.links = []

    def draw(self, surface, camera):
        pygame.draw.line(surface, self.color, camera.transform(self.end1), camera.transform(self.end2))

    @property
    def end1(self):
        return Pt(0, 0)

    @property
    def end2(self):
        return Pt(0, 0)


class HLine(Line):
    def __init__(self, y, x1, x2):
        Line.__init__(self)

        if x1 > x2:
            x1, x2 = x2, x1

        self.y = y
        self.x1 = x1
        self.x2 = x2

    @property
    def end1(self):
        return Pt(self.x1, self.y)

    @property
    def end2(self):
        return Pt(self.x2, self.y)

    def draw(self, surface, camera):
        Line.draw(self, surface, camera)

        l_color = (200, 0, 0)

        for l in self.links:
            l_pt = Pt(l.x, self.y)

            pygame.draw.line(surface, l_color, camera.transform(l_pt + (10, 10)), camera.transform(l_pt + (-10, 10)))
            pygame.draw.line(surface, l_color, camera.transform(l_pt + (10, -10)), camera.transform(l_pt + (-10, -10)))

    def try_move(self, pos):
        if pos.x < self.x1:
            return self.end1
        if pos.x > self.x2:
            return self.end2
        return Pt(pos.x, self.y)

    def closest_link(self, to, condition=None):
        if condition is None:
            condition = lambda l: True
        dist = x_dist_to(to.x)
        lts = sorted([l for l in self.links if condition(l)], key=dist)
        if lts:
            return lts[0], dist(lts[0])
        else:
            return None, max_dist

    def up_closest(self, to):
        return self.closest_link(to, lambda l: l.y2 > self.y)

    def down_closest(self, to):
        return self.closest_link(to, lambda l: l.y1 < self.y)


class VLine(Line):
    def __init__(self, x, y1, y2):
        Line.__init__(self)

        if y1 > y2:
            y1, y2 = y2, y1

        self.x = x
        self.y1 = y1
        self.y2 = y2

    @property
    def end1(self):
        return Pt(self.x, self.y1)

    @property
    def end2(self):
        return Pt(self.x, self.y2)

    def draw(self, surface, camera):
        Line.draw(self, surface, camera)

        l_color = (200, 0, 0)

        for l in self.links:
            l_pt = Pt(self.x, l.y)

            pygame.draw.line(surface, l_color, camera.transform(l_pt + (10, -10)), camera.transform(l_pt + (10, 10)))
            pygame.draw.line(surface, l_color, camera.transform(l_pt + (-10, -10)), camera.transform(l_pt + (-10, 10)))

    def try_move(self, pos):
        if pos.y < self.y1:
            return self.end1
        if pos.y > self.y2:
            return self.end2
        return Pt(self.x, pos.y)

    def closest_link(self, to, condition=None):
        if condition is None:
            condition = lambda l: True
        dist = y_dist_to(to.y)
        lts = sorted([l for l in self.links if condition(l)], key=dist)
        if lts:
            return lts[0], dist(lts[0])
        else:
            return None, max_dist

    def left_closest(self, to):
        return self.closest_link(to, lambda l: l.x1 < self.x)

    def right_closest(self, to):
        return self.closest_link(to, lambda l: l.x2 > self.x)


def x_dist_to(x):
    return lambda vline: abs(vline.x - x)


def y_dist_to(y):
    return lambda hline: abs(hline.y - y)
