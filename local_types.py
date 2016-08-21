class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '<{},{}>'.format(self.x, self.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Position):
            return Position(self.x * other.x, self.y * other.y)

        return Position(self.x * other, self.y * other)

    @property
    def t(self):
        return self.x, self.y
