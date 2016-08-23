from local_types import Pt
import pygame


def marker(pt, surface):
    # pt = Pt(pt)
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(-5, 0))
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(5, 0))
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(0, 5))
    pygame.draw.line(surface, pygame.Color('red'), pt, pt + Pt(0, -5))
