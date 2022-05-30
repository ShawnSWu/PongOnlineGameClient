import pygame


class MenuOption:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y


def game_text(text, bg_color):
    font = pygame.font.Font('font/coders_crux.ttf', 50)
    return font.render(text, True, (203, 202, 203), bg_color)


class MainMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.menu_option = [
            MenuOption('Start', (screen_width / 2) - 52, (screen_height / 2 + 120)),
            MenuOption('Online Game', (screen_width / 2) - 105, (screen_height / 2 + 155)),
            MenuOption('Quit', (screen_width / 2) - 40, (screen_height / 2 + 190))
        ]
        self.selected = 0
        self.selected_color = (74, 74, 74)
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

    def previous(self):
        if self.selected >= 1:
            self.selected -= 1

    def next(self):
        if self.selected < len(self.menu_option) - 1:
            self.selected += 1

    def update_menu(self):
        for i, v in enumerate(self.menu_option):
            if i == self.selected:
                text_start = game_text(v.text, self.selected_color)
                self.screen.blit(text_start, (v.x, v.y))
            else:
                text_start = game_text(v.text, (38, 38, 38))
                self.screen.blit(text_start, (v.x, v.y))



