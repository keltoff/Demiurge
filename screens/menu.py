from screen import Screen
import pygame.draw as draw
import pygame.font as font
from pygame import Rect


class MenuScreen(Screen):
    def draw(self, surface):
        self.bar(surface, 'New game', (50, 200))
        self.bar(surface, 'Continue', (50, 300))
        self.bar(surface, 'Exit', (50, 400))

    def bar(self, surface, text, pos, w=300):
        rect = Rect(pos, (w, 60))
        draw.rect(surface, (0, 200, 200), rect)

        sf = font.SysFont('blah', 60, bold=False, italic=False)
        txt = sf.render(text, True, (0, 0, 0))
        surface.blit(txt, rect.inflate(-10, -10))
