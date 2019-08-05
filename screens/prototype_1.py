from graphics import camera as cam
from level.linkage_level import Linkage
import pygame
import pygame.locals
import pygame.draw as draw
import pygame.font as font
from pygame import Rect
from graphics.background import empty
import GUI as gui
from local_types import Pt
import sprites.sophia as soph
from screen import Screen


class BoxPrototypeScreen(Screen):
    def __init__(self):
        self.background = empty()

        self.level = Linkage.from_xml('data/prototyp_1.xml')

        self.gui = gui.GUI()

        self.camera = cam.Camera(Pt(320, 240))
        self.focus = None

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

        if release:
            return

        if key == pygame.K_HOME:
            self.focus = None
            self.camera.focus_on(Pt(0, 0))
        if key == pygame.K_PAGEDOWN:
            if self.focus is None or self.focus == len(self.level.bodies)-1:
                self.focus = 0
            else:
                self.focus += 1
            self.camera.focus_on(self.level.bodies[self.focus])
        if key == pygame.K_PAGEUP:
            if self.focus is None or self.focus == 0:
                self.focus = len(self.level.bodies) - 1
            else:
                self.focus -= 1
            self.camera.focus_on(self.level.bodies[self.focus])

        # self.player.control(pressed)
        motions = {'UP': (0, 10), 'DN': (0, -10), 'LT': (-10, 0), 'RT': (10, 0)}
        if pressed in motions.keys():
            self.focus = None
            self.camera.target = self.camera.pos + motions[pressed]


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
