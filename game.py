from screens import screen

__author__ = 'tryid_000'

import pygame
import pygame.locals


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((640, 480))

    clock = pygame.time.Clock()

    # overlays = pygame.sprite.RenderUpdates()
    # pygame.display.flip()

    menu = screen.MenuScreen()
    game = screen.GameScreen()
    # currentScreen = menu
    currentScreen = game

    game_over = False
    while not game_over:

        # XXX draw all the objects here
        currentScreen.update()
        currentScreen.draw(display)

        # overlays = pygame.sprite.RenderUpdates()
        # overlays.draw(screen)
        pygame.display.flip()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            elif event.type == pygame.locals.KEYDOWN:
                currentScreen.handle_key(event.key)
            elif event.type == pygame.locals.KEYUP:
                currentScreen.handle_key(event.key, release=True)