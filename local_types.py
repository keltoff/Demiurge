import operator


# class Position:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def __str__(self):
#         return '<{},{}>'.format(self.x, self.y)
#
#     def __add__(self, other):
#         return Position(self.x + other.x, self.y + other.y)
#
#     def __sub__(self, other):
#         return Position(self.x - other.x, self.y - other.y)
#
#     def __mul__(self, other):
#         if isinstance(other, Position):
#             return Position(self.x * other.x, self.y * other.y)
#
#         return Position(self.x * other, self.y * other)
#
#     @property
#     def t(self):
#         return self.x, self.y


def add(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return x1+x2, y1+y2


def neg(pt):
    x, y = pt
    return -x, -y


def mul(pt, k):
    x, y = pt
    return x*k, y*k


def div(pt, k):
    x, y = pt
    return x/k, y/k


class Pt(tuple):
    def __new__(self, *T):
        if len(T) == 1 and T[0].__class__ == tuple is tuple:
            return tuple.__new__(Pt, *T)
        else:
            return tuple.__new__(Pt, T)

    def __add__(self, other):
        return Pt(add(self, other))

    def __neg__(self):
        return Pt(neg(self))

    def __sub__(self, other):
        return self + neg(other)

    def __mul__(self, other):
        if hasattr(other, '__len__') and len(other) == 2:
            return Pt(self[0] * other[0], self[1] * other[1])
        else:
            return Pt(mul(self, other))

    def __truediv__(self, other):
        return Pt(div(self, other))

    def as_int(self):
        return Pt(int(self[0]), int(self[1]))


Pt.x = property(operator.itemgetter(0))
Pt.y = property(operator.itemgetter(1))


class FlipThroughList:
    def __init__(self, content):
        self.content = content
        self.current = None

    def __getitem__(self, item):
        return self.content.__getitem__(item)

    def next(self):
        if self.current in [None, len(self.content) -1 ]:
            self.current = 0
        else:
            self.current += 1

        return self.item

    def last(self):
        if self.current in [None, 0 ]:
            self.current = len(self.content) - 1
        else:
            self.current -= 1

        return self.item

    def clear(self):
        self.current = None
        return None

    @property
    def item(self):
        if self.current is None:
            return None
        else:
            return self.content[self.current]