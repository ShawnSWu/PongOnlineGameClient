import threading

import pygame

from online.payload.Payload import *
from view.BasicView import BasicView
from view.panel.PlayerPanel import PlayerPanel

lock = threading.Lock()

ReadyBattle = 0
LeaveRoom = 1

class RoomView(BasicView):
    def __init__(self, screen, socket_conn):
        super().__init__(screen)
        self.bg_color = (38, 38, 38)
        self.socket_conn = socket_conn
        self.room_id = -1
        self.selected = 0
        self.selected_color = (65, 105, 105)
        self.players = create_empty_player_panel()

    def update_players(self, room_in_model):
        room_id = room_in_model.room_id
        room_name = room_in_model.room_name
        self.room_id = room_id

        player1_id = room_in_model.player1_id
        player1_name = room_in_model.player1_name
        player1_ready_status = room_in_model.player1_ready_status
        player2_id = room_in_model.player2_id
        player2_name = room_in_model.player2_name
        player2_ready_status = room_in_model.player2_ready_status

        player1 = self.players[0]
        player1.player_id = player1_id
        player1.player_name = player1_name
        player1.ready_status = player1_ready_status

        if player1.player_id != '':
            player1.display = True

        player2 = self.players[1]
        player2.player_id = player2_id
        player2.player_name = player2_name
        player2.ready_status = player2_ready_status

        if player2.player_id != '':
            player2.display = True

    def listen_player_operation(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                self.handle_operation(event)

    def handle_operation(self, event):
        if event.key == pygame.K_UP:
            if self.selected > 0:
                self.clear_view(self.bg_color)
                self.draw()
                self.draw_ready_button(self.selected_color)
                self.draw_leave_button(None)
                pygame.display.update()
                self.selected -= 1

        elif event.key == pygame.K_DOWN:
            if self.selected <= 0:
                self.clear_view(self.bg_color)
                self.draw()
                self.draw_ready_button(None)
                self.draw_leave_button(self.selected_color)
                self.selected += 1
                pygame.display.update()

        elif event.key == pygame.K_RETURN:
            if self.room_id != -1:
                if self.selected == ReadyBattle:
                    self.ready_battle(self.room_id)
                elif self.selected == LeaveRoom:
                    self.leave_room(self.room_id)

    def draw_ready_button(self, bg_color):
        self.draw_game_text("READY TO BATTLE", 295, 500, 50, bg_color)

    def draw_leave_button(self, bg_color):
        self.draw_game_text("LEAVE", 360, 540, 50, bg_color)

    def draw(self):
        lock.acquire()
        self.clear_view(self.bg_color)

        if self.selected == 0:
            self.draw_ready_button(self.selected_color)
            self.draw_leave_button(None)
        elif self.selected == 1:
            self.draw_ready_button(None)
            self.draw_leave_button(self.selected_color)

        for i, r in enumerate(self.players):
            if r.display is not False:
                # 方格
                self.draw_rect(r.x, r.y, r.width, r.height, r.bg_color)

                name = r.player_name
                name_x = r.name_text_location[0]
                name_y = r.name_text_location[1]
                self.draw_game_text(name, name_x, name_y, 30)

                icon_x = r.icon_location[0]
                icon_y = r.icon_location[1]
                if i == 0:
                    self.draw_image(r'img/player1.png', icon_x, icon_y)
                else:
                    self.draw_image(r'img/player2.png', icon_x, icon_y)
        lock.release()

    def ready_battle(self, room_id):
        payload = ready_battle_payload_template(room_id)
        self.socket_conn.send(str.encode(payload))

    def leave_room(self, room_id):
        payload = leave_room_payload_template(room_id)
        self.socket_conn.send(str.encode(payload))


def create_empty_player_panel():
    return [
        PlayerPanel(41, 47, player_name='', name_text_location=(240, 85), icon_location=(44, 112)),
        PlayerPanel(423, 47, player_name='', name_text_location=(622, 85), icon_location=(472, 112)),
    ]
