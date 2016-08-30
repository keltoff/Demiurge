from local_types import Pt
import pygame


def marker(pt, surface):
    # pt = Pt(pt)
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(-5, 0))
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(5, 0))
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(0, 5))
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(0, -5))


def anchored_rect(position, shape, anchor='cc'):
    if isinstance(shape, pygame.Rect):
        rect = shape
    else:
        rect = pygame.Rect((0, 0), shape)

    # TODO posunout podle anchoru

    return rect

