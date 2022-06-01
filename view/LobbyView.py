import threading

import pygame

from online.payload.Payload import *
from view.BasicView import BasicView, GameText
from view.panel.RoomItemPanel import RoomItemPanel

lock = threading.Lock()

class LobbyView(BasicView):
    def __init__(self, screen, socket_conn):
        super().__init__(screen)
        self.socket_conn = socket_conn
        self.bg_color = (38, 38, 38)
        self.rooms_panel = create_empty_room_panel()
        self.rooms_data = []
        self.selected = 0
        self.online_player_count = 0
        self.selected_color = (65, 105, 105)

    def update_rooms_data(self, room_list):
        lock.acquire()
        self.rooms_data = room_list
        updated_rooms_count = len(room_list)

        for i in range(len(self.rooms_panel)):
            if i < updated_rooms_count:
                self.rooms_panel[i].room_name_text.text = room_list[i].room_name
                self.rooms_panel[i].room_status_text.text = room_list[i].room_status
                self.rooms_panel[i].crate_date_text.text = room_list[i].create_date
                self.rooms_panel[i].player_count_text.text = room_list[i].player_count
                self.rooms_panel[i].display = True
            else:
                self.rooms_panel[i].display = False

        lock.release()

    def draw(self):
        lock.acquire()
        self.clear_view(self.bg_color)
        if self.get_room_count() == 0:
            self.display_no_room()
        if self.selected == self.get_room_count():
            self.draw_create_room_button(self.selected_color)
            self.draw_leave_room_button(None)
        elif self.selected == self.get_room_count() + 1:
            self.draw_create_room_button(None)
            self.draw_leave_room_button(self.selected_color)
        else:
            self.draw_create_room_button(None)
            self.draw_leave_room_button(None)
        for i, r in enumerate(self.rooms_panel):
            if r.display is True:
                # 方格
                room_rect = pygame.Rect(r.x, r.y, r.width, r.height)

                if self.selected == i:
                    pygame.draw.rect(self.screen, self.selected_color, room_rect, 0)
                else:
                    pygame.draw.rect(self.screen, (110, 110, 110), room_rect, 0)

                rn = r.room_name_text
                self.draw_game_text(str(rn.text), (rn.x[0]), rn.y[0], (rn.size[0]))

                cd = r.crate_date_text
                self.draw_game_text(str(cd.text[5:len(cd.text) - 1]), (cd.x[0]), (cd.y[0]), (cd.size[0]))

                pc = r.player_count_text
                self.draw_game_text(str(pc.text) + "/2", (pc.x[0]), (pc.y[0]), (pc.size[0]))

                rs = r.room_status_text
                self.draw_game_text(_mapping_room_status(str(rs.text)), (rs.x[0]), (rs.y[0]), (rs.size[0]))

                self.draw_image(r'img/swords.png', r.icon_location[0], r.icon_location[1])

        # 顯示線上人數
        current_player_count = "Current online player:{count}".format(count=self.online_player_count)
        self.draw_game_text(current_player_count, x=545, y=15, size=25)

        self.screen_update_view()
        lock.release()


    def get_room_count(self):
        return len(self.rooms_data)

    def display_no_room(self):
        self.clear_view(self.bg_color)

        width, height = self.screen.get_size()
        self.draw_game_text("No Room", width / 2 - 100, height / 2 - 50, 60)

    def select_previous_room(self):
        if self.selected >= 1:
            self.selected -= 1

    def select_next_room(self):
        if self.selected <= self.get_room_count():
            self.selected += 1

    def draw_create_room_button(self, bg_color):
        self.draw_game_text("CREATE ROOM", 295, 500, 50, bg_color)

    def draw_leave_room_button(self, bg_color):
        self.draw_game_text("LEAVE", 360, 540, 50, bg_color)

    def listen_player_operation(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.handle_operation(event)

    def handle_operation(self, event):
        if event.key == pygame.K_UP:
            self.select_previous_room()
        elif event.key == pygame.K_DOWN:
            self.select_next_room()
        elif event.key == pygame.K_RETURN:
            if self.selected == self.get_room_count():
                # 創建房間
                print("創建房間")
                room_name = "My ROOM"
                self.create_room(self.socket_conn, room_name)
            elif self.selected == self.get_room_count() + 1:
                # 離開大廳
                self.leave_lobby(self.socket_conn)
            else:
                # 進入房間
                room_id = self.rooms_data[self.selected].room_id
                self.enter_room(self.socket_conn, room_id)


    def create_room(self, conn, room_name):
        payload = create_room_payload_template(room_name)
        print(payload)
        conn.send(str.encode(payload))

    def leave_lobby(self, conn):
        payload = leave_lobby_payload_template()
        conn.send(str.encode(payload))

    def enter_room(self, conn, room_id):
        payload = enter_room_payload_template(room_id)
        conn.send(str.encode(payload))


def _mapping_room_status(room_status):
    if room_status == "0":
        return "Waiting"
    else:
        return "Playing"


def create_empty_room_panel():
    return [
        RoomItemPanel(x=38, y=42,
                      room_name_text=GameText('', 51, 60, 45),
                      player_count_text=GameText('', 306, 60, 40),
                      crate_date_text=GameText('', 51, 122, 35),
                      room_status_text=GameText('', 265, 122, 35),
                      icon_location=(230, 55)),

        RoomItemPanel(x=38, y=193,
                      room_name_text=GameText('', 51, 210, 45),
                      player_count_text=GameText('', 306, 210, 40),
                      crate_date_text=GameText('', 51, 270, 35),
                      room_status_text=GameText('', 265, 270, 35),
                      icon_location=(230, 205)),

        RoomItemPanel(x=38, y=344,
                      room_name_text=GameText('', 51, 360, 45),
                      player_count_text=GameText('', 306, 360, 40),
                      crate_date_text=GameText('', 51, 420, 35),
                      room_status_text=GameText('', 265, 420, 35),
                      icon_location=(230, 353)),

        RoomItemPanel(x=414, y=42,
                      room_name_text=GameText('', 430, 60, 45),
                      player_count_text=GameText('', 683, 60, 40),
                      crate_date_text=GameText('', 427, 122, 35),
                      room_status_text=GameText('', 644, 122, 35),
                      icon_location=(610, 52)),

        RoomItemPanel(x=414, y=193,
                      room_name_text=GameText('', 430, 210, 45),
                      player_count_text=GameText('', 683, 210, 40),
                      crate_date_text=GameText('', 427, 270, 35),
                      room_status_text=GameText('', 644, 270, 35),
                      icon_location=(610, 202)),

        RoomItemPanel(x=414, y=344,
                      room_name_text=GameText('', 430, 360, 45),
                      player_count_text=GameText('', 683, 360, 40),
                      crate_date_text=GameText('', 427, 420, 35),
                      room_status_text=GameText('', 644, 420, 35),
                      icon_location=(610, 353)),
    ]
