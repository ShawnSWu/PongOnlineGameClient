import sys

import re
import pygame

from menu.MainMenu import MainMenu
from pygame.locals import *
from menu.OnlineMenu import OnlineMenu
from online.Client import Client
from view.BasicView import BasicView
from view.LobbyView import LobbyView

bg_color = (38, 38, 38)

game_name = 'P O N G'
game_icon = r'img/pong_icon.png'


class StartView(BasicView):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg_color = (38, 38, 38)

    def start(self):
        self.clear_view(self.bg_color)
        self.draw_game_title()
        self.draw_main_menu()

    def draw_game_title(self):
        # Game Title
        width, height = self.screen.get_size()
        self.draw_game_text(game_name, (width / 2) - 180, height / 8 - 10, 140)
        self.draw_image(game_icon, 280, 145)

    def update_player_input(self, om, value):
        self.clear_view(bg_color)
        self.draw_game_title()
        om.change_input_text(value)
        om.draw_menu()
        self.screen_update_view()

    def draw_online_option(self):
        self.clear_view(bg_color)
        self.draw_game_title()

        width, height = self.screen.get_size()
        om = OnlineMenu(self.screen, width, height)
        om.draw_menu()
        self.screen_update_view()

        self.listen_online_menu(om)

    def listen_online_menu(self, om):
        self.listen_input_box_player_name(om)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if om.selected >= 1:
                            om.previous()
                            om.draw_menu()
                            self.screen_update_view()

                            if om.selected == 1:
                                self.listen_input_box_player_name(om)
                                om.next()
                                om.draw_menu()

                    elif event.key == pygame.K_DOWN:
                        if om.selected < len(om.menu_option) - 1:
                            om.next()
                            om.draw_menu()

                    if event.key == pygame.K_RETURN:
                        if om.selected == 2:
                            input = om.menu_option[1].text
                            re_result = re.fullmatch(r'^\w+', input)
                            if re_result is not None:
                                player_name = om.menu_option[1].text

                                if len(player_name) > 0 and len(player_name) <= 6:
                                    c = Client(self.screen)
                                    is_leave_lobby = c.start_online_game(player_name)
                                    if is_leave_lobby is False:
                                        self.start()

                        elif om.selected == 3:
                            self.clear_view(bg_color)
                            self.draw_game_title()
                            self.draw_main_menu()
            self.screen_update_view()

    def listen_input_box_player_name(self, om):
        value = ""
        while True:
            for evt in pygame.event.get():
                if evt.type == KEYDOWN:
                    if evt.unicode.isalpha():
                        value += evt.unicode
                        self.update_player_input(om, value)
                    elif evt.key == K_BACKSPACE:
                        value = value[:-1]
                        self.update_player_input(om, value)
                    elif evt.key == K_DOWN:
                        return

    def draw_main_menu(self):
        width, height = self.screen.get_size()
        menu = MainMenu(self.screen, width, height)
        menu.draw_menu()
        self.screen_update_view()

        # ??????main menu??????
        self.listen_main_menu_operation(menu)

    def listen_main_menu_operation(self, menu):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        menu.previous()
                        menu.draw_menu()
                    elif event.key == pygame.K_DOWN:
                        menu.next()
                        menu.draw_menu()

                    if event.key == pygame.K_RETURN:
                        if menu.selected == 0:
                            # ????????????
                            pass
                        elif menu.selected == 1:
                            self.draw_online_option()
                            pass
                        elif menu.selected == 2:
                            sys.exit()
                            pass
            pygame.display.update()

