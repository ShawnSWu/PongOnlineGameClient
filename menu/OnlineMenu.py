import pygame

from menu.BasicMenu import MenuOption


def game_text(text, bg_color):
    font = pygame.font.Font('font/coders_crux.ttf', 50)
    return font.render(text, True, (203, 202, 203), bg_color)


class OnlineMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.menu_option = [
            MenuOption('Name:', 291, 415),
            MenuOption(' ', 385, 415),
            MenuOption('Enter', 350, 457),
            MenuOption('Exit', 365, 495)
        ]
        self.selected = 1
        self.selected_color = (74, 74, 74)
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def previous(self):
        if self.selected > 1:
            self.selected -= 1

    def next(self):
        if self.selected < len(self.menu_option) - 1:
            self.selected += 1

    def draw_menu(self):
        for i, v in enumerate(self.menu_option):
            if i == self.selected:
                if len(self.menu_option[1].text) > 6:
                    text_start = game_text(v.text, (255, 74, 74))
                else:
                    text_start = game_text(v.text, self.selected_color)
                self.screen.blit(text_start, (v.x, v.y))
            else:
                text_start = game_text(v.text, (38, 38, 38))
                self.screen.blit(text_start, (v.x, v.y))

    def change_input_text(self, value):
        self.menu_option[1].text = value
