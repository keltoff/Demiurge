# import pygame.Sprite
from pygame import Rect
import pygame.draw
from local_types import Position
import level.lines as lines


class state():
    def __init__(self, name, img, shift, hold=None, end='last', speed=None):
        self.sprite = None
        self.name = name
        self.img = img
        self.shift = shift
        self.hold = hold

        self.end = end

        if speed is None:
            self.speed = Position(0, 0)
        else:
            self.speed = speed
        # self.animation = None

    def __str__(self):
        return self.name

    def control(self, pressed):
        if pressed in self.shift:
            self.sprite.shift(self.shift[pressed])


# class sophia(pygame.Sprite):
class sophia():
    def __init__(self):
        self.pos = Position(0, 0)
        self.radius = Position(15, -25)
        self.rect = Rect(0, 0, 30, 50)
        self.speed = 10
        self.stick = None

        self.jump_height_left = 0

        self.states = dict()

        base = {'LT': 'left_run', 'RT': 'right_run', 'UP':'back'}
        left = {'JMP': 'left_jump', 'DN': 'left_crouch', 'drop': 'left_fall'}
        right = {'JMP': 'right_jump', 'DN': 'right_crouch', 'drop': 'right_fall'}

        self.add_state(state('left', img=1, shift=_merge_(base, left, {'LT': 'left_run'})))
        self.add_state(state('left_run', img=3, hold='LT', end='left', speed=Position(-self.speed, 0),
                                         shift=_merge_(base, left, {'DN': 'left_slide', 'hit_L': 'left', 'JMP': 'left_jump_l'})))
        self.add_state(state('left_crouch', img=4, hold='DN', end='left', shift={'LT': 'left_slide'}))
        self.add_state(state('left_jump', img=5, speed=Position(0, 15), hold='JMP', end='left_fall', shift={'RT': 'right_jump_r'}))
        self.add_state(state('left_jump_l', img=5, speed=Position(-5, 15), hold='LT', end='left_jump', shift={'RT': 'right_jump_r'}))
        self.add_state(state('left_fall', img=1, speed=Position(0, -5), end='left', shift={'hit_D': 'left', 'LT': 'left_fall_l', 'RT': 'right_fall_r'}))
        self.add_state(state('left_fall_l', img=1, speed=Position(-5, -5), hold='LT', end='left_fall', shift={'hit_D': 'left_run', 'RT': 'right_fall_r'}))

        self.add_state(state('right', img=1, shift=_merge_(base, right, {'RT':'right_run'})))
        self.add_state(state('right_run', img=3, hold='RT', end='right', speed=Position(self.speed, 0),
                                          shift=_merge_(base, right, {'DN': 'right_slide'})))
        self.add_state(state('right_crouch', img=4, hold='DN', end='right', shift={'RT': 'right_slide'}))
        self.add_state(state('right_jump', img=5, speed=Position(0, 15), hold='JMP', end='right_fall', shift={'LT': 'left_jump_l'}))
        self.add_state(state('right_jump_r', img=5, speed=Position(5, 15), hold='left', end='right_jump', shift={'LT': 'left_jump_l'}))
        self.add_state(state('right_fall', img=1, speed=Position(0, -5), end='right', shift={'hit_D': 'right', 'LT': 'left_fall_l', 'RT': 'right_fall_r'}))
        self.add_state(state('right_fall_r', img=1, speed=Position(5, -5), hold='RT', end='right_fall', shift={'hit_D': 'right_run', 'LT': 'left_fall_l'}))

        self.add_state(state('back', img=10, hold='DN', end='left', shift=base))

        # self.add_state(state('blastoff', img=12, speed=Position(0, 12), shift={'DN':'left'}))

        self.state = self.states['left']

        self.sprites = self.load_img()

    @property
    def cpos(self):
        return self.pos - self.radius

    def control(self, command):

        if command in ['JMP']:
            self.jump_height_left = 200  # max jump height - get from level?

        self.state.control(command)

    def update(self, level, keys):

        if self.state.hold not in keys:
            self.shift(self.state.end)

        # v = self.state.speed + level.G
        v = self.state.speed
        self.pos, hit = level.can_move(self.pos, v, h=self.radius.x, w=-self.radius.y, constraint=self.stick)

        if self.jump_height_left > 0:
            self.jump_height_left -= v[1]
        if self.jump_height_left <= 0:
            self.jump_height_left = 0
            self.control('fall')

        for (c, p) in hit:
            if c in ['drop', 'JMP']:
                self.stick = None
                # self.shift('left_fall')
            elif c == 'hit_D':
                self.stick = p
                # self.shift('left')

            self.control(c, [])

    def draw(self, surface, camera):
        tpos = camera.transform(self.cpos)
        sprite = self.sprites[self.state.name]
        surface.blit(sprite, tpos)

        if self.stick is not None:
            lines.drawline(surface, (0, 250, 0), camera, self.stick)

        # cp = camera.transform(self.cpos)
        # sr = self.rect.move(cp)
        # pygame.draw.rect(surface, (0, 200, 0), sr)

        # tp = camera.transform(self.pos)
        # pygame.draw.line(surface, (200, 0, 0), (tp[0], tp[1]-10), (tp[0], tp[1]+10))
        # pygame.draw.line(surface, (200, 0, 0), (tp[0]-10, tp[1]), (tp[0]+10, tp[1]))

    def shift(self, new_state):
        if new_state in self.states:
            # self.states['last'] = self.state
            self.state = self.states[new_state]

            w, h = self.sprites[new_state].get_size()
            # self.radius = Position(w/2, -h/2)

            print('shift to: {}'.format(new_state))
        else:
            print('No such state: {}'.format(new_state))

    def add_state(self, state):
        self.states[state.name] = state
        state.sprite = self

    def load_img(self):
        filename = 'sprites/mega.gif'
        height, width = 80, 60
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        table = dict()
        # for tile_x in range(0, image_width/width):
        #     for tile_y in range(0, image_height/height):
        #         rect = (tile_x*width, tile_y*height, width, height)
        #         table.append(image.subsurface(rect))

        table['left'] = image.subsurface((256, 100, 33, 40))
        table['left_run'] = image.subsurface((218, 100, 30, 40))
        table['left_crouch'] = image.subsurface((156, 280, 30, 36))
        table['left_jump'] = image.subsurface((226, 230, 30, 50))
        table['left_jump_l'] = table['left_jump']
        table['left_fall'] = image.subsurface((150, 222, 30, 55))
        table['left_fall_l'] = table['left_fall']

        table['right'] = image.subsurface((298, 100, 33, 40))
        table['right_run'] = image.subsurface((370, 100, 40, 40))
        table['right_crouch'] = image.subsurface((400, 280, 30, 36))
        table['right_jump'] = image.subsurface((326, 230, 30, 50))
        table['right_jump_r'] = table['right_jump']
        table['right_fall'] = image.subsurface((402, 222, 30, 55))
        table['right_fall_r'] = table['right_fall']
        
        table['back'] = image.subsurface((176, 577, 30, 50))
        return table


def _merge_(dict, *args):
    res = dict.copy()
    for a in args:
        res.update(a)
    return res
