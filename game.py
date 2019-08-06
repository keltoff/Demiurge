from screens.menu import MenuScreen
from screens.game import GameScreen
from screens.prototype_1 import BoxPrototypeScreen
__author__ = 'tryid_000'

import pygame
import pygame.locals


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((640, 480))

    clock = pygame.time.Clock()

    # overlays = pygame.sprite.RenderUpdates()
    # pygame.display.flip()

    # menu = MenuScreen()
    # game = GameScreen()

    # currentScreen = menu
    # currentScreen = game

    prototype = BoxPrototypeScreen()
    current_screen = prototype

    game_over = False
    while not game_over:

        # XXX draw all the objects here
        current_screen.update()
        current_screen.draw(display)

        # overlays = pygame.sprite.RenderUpdates()
        # overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                current_screen.handle_key(event.key)
                if event.key == pygame.K_q:
                    game_over = True
            elif event.type == pygame.locals.KEYUP:
                current_screen.handle_key(event.key, release=True)
