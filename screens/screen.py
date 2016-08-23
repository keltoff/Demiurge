from graphics import camera as cam
from level.lines import Lines
import pygame
import pygame.locals
import pygame.draw as draw
import pygame.font as font
from pygame import Rect
from graphics.background import empty
import GUI as gui
from local_types import Pt
import sprites.sophia as soph


class Screen:
    def __init__(self):
        pass

    def draw(self, surface):
        pass

    def update(self):
        pass

    def handle_key(self, key, release=False):
        pass


class GameScreen(Screen):
    def __init__(self):
        self.background = empty()

        self.level = Lines.from_xml()

        self.gui = gui.GUI()

        self.camera = cam.Camera(Pt(320, 240))

        # sophia = soph.sophia()
        # sophia.pos = Position(10, 10)

        # self.player = sophia
        # self.sprites = [sophia]
        self.sprites = []

    def update(self):
        held_keys = _keys_held()

        for s in self.sprites:
            s.update(self.level, held_keys)
        self.camera.update()

    def draw(self, surface):

        self.background.draw(surface, self.camera)
        self.level.draw(surface, self.camera)
        for s in self.sprites:
            s.draw(surface, self.camera)

        # self.effects.draw()
        self.gui.draw(surface)

    def handle_key(self, key, release=False):
        pressed = _key_transform_(key)

        if key == pygame.K_HOME:
            self.camera.focus_on(self.player)
        if key == pygame.K_INSERT:
            self.camera.focus_on(Pt(0, 0))
        if key == pygame.K_PAGEUP:
            self.camera.focus_on(Pt(400, 200))

        if release == False:
            self.player.control(pressed)

        # if release:
        #     self.player.control(None, held)
            # self.player.control(pressed, held)
        # else:
        #     self.player.control(pressed, held)


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


_keymap_ = {pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DN',
            pygame.K_LEFT: 'LT',
            pygame.K_RIGHT: 'RT',
            pygame.K_z: 'JMP'}


def _key_transform_(pressed):
    return _keymap_.get(pressed, None)


def _keys_held():
    held = []
    state = pygame.key.get_pressed()

    for k, v in _keymap_.items():
        if state[k]:
            held.append(v)

    return held
