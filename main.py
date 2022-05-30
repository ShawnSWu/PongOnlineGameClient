import pygame

from view.BasicView import BasicView
from view.StartView import StartView

if __name__ == '__main__':
    pygame.init()

    game_name = 'P O N G'
    screen_width, screen_height = 800, 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(game_name)

    basic_view = BasicView(screen)
    StartView(screen).start()
