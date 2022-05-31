import pygame


class BasicView(object):
    def __init__(self, screen):
        self.screen = screen
        self.FPS = 120

    def get_width_height(self):
        width, height = self.screen.get_size()
        return width, height

    def clear_view(self, bg_color):
        self.screen.fill(bg_color)

    def draw_game_text(self, game_text, x, y, size, bg_color=None, text_color=(203, 202, 203)):
        head_font = pygame.font.Font('font/coders_crux.ttf', size)
        self.screen.blit(head_font.render(str(game_text), True, text_color, bg_color), (x, y))

    def draw_rect(self, x, y, width, height, color):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, 0)

    def draw_image(self, image, w, h):
        self.screen.blit(pygame.image.load(image), (w, h))

    def screen_update_view(self):
        pygame.display.update()



class GameText:
    def __init__(self, text, x, y, size):
        self.text = text,
        self.x = x,
        self.y = y,
        self.size = size,
