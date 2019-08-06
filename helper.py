from local_types import Pt
import pygame


def marker(pt, surface, mark='+', color='red'):
    if isinstance(color, str):
        color = pygame.Color(color)

    size = 5

    if mark == '+':
        pygame.draw.line(surface,  color, pt, pt + Pt(-size, 0))
        pygame.draw.line(surface, color, pt, pt + Pt(size, 0))
        pygame.draw.line(surface, color, pt, pt + Pt(0, size))
        pygame.draw.line(surface, color, pt, pt + Pt(0, -size))
    elif mark == 'o':
        pygame.draw.circle(surface, color, pt.as_int(), size, 1)
    elif mark == 'x':
        pygame.draw.line(surface, color, pt, pt + Pt(-size, -size))
        pygame.draw.line(surface, color, pt, pt + Pt(-size, size))
        pygame.draw.line(surface, color, pt, pt + Pt(size, -size))
        pygame.draw.line(surface, color, pt, pt + Pt(size, size))


def anchored_rect(position, shape, anchor='cc'):
    if isinstance(shape, pygame.Rect):
        rect = shape
    else:
        rect = pygame.Rect((0, 0), shape)

    # TODO posunout podle anchoru

    return rect

