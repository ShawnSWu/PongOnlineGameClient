import json
import threading
import socket
import time

import pygame

from online.payload import Payload
from online.payload.Payload import parse_room_list, parse_player_list, parse_battle_info, parse_battle_over, \
    parse_online_player_count, set_player_name_payload_template
from view.BattleView import BattleView
from view.LobbyView import LobbyView
from view.RoomView import RoomView

SceneHome = 'HOME'
SceneLobby = 'LOBBY'
SceneRoom = 'ROOM'
SceneBattle = 'BATTLE'
SceneCountDownBattle = 'COUNT_DOWN_BATTLE'

lock = threading.Lock()


class Client:
    def __init__(self, screen):
        self.screen = screen
        self.player_name = ''
        self.lobby = None
        self.room = None
        self.battle = None
        self.scene = SceneLobby
        self.FPS = 120
        pass

    def start_online_game(self, player_name):
        self.player_name = player_name

        # 連線Server
        socket_conn = self.connect_server()

        if socket_conn is False:
            show_server_not_work_msg(self.screen)
            return

        set_player_name(socket_conn, player_name)

        self.lobby = LobbyView(self.screen, socket_conn, self.player_name)
        self.room = RoomView(self.screen, socket_conn)
        self.battle = BattleView(self.screen, socket_conn)

        # 監聽Server回應
        listen_server_thread = threading.Thread(target=self.listen_server_payload, args=(socket_conn,))
        listen_server_thread.start()

        # 心跳封包
        heart_beat_thread = threading.Thread(target=heart_beat_job, args=(socket_conn,))
        heart_beat_thread.start()

        clock = pygame.time.Clock()
        # Lobby Loop
        while True:
            clock.tick(600)

            if self.scene == SceneLobby:
                self.lobby.listen_player_operation()
                self.lobby.draw()

            elif self.scene == SceneRoom:
                self.room.listen_player_operation()
                self.room.draw()

            elif self.scene == SceneBattle:
                self.battle.listen_player_operation()
                self.battle.draw()

            elif self.scene == SceneCountDownBattle:
                self.battle.draw_battle_ready_start_hint()

            elif self.scene == SceneHome:
                break

            self.lobby.screen_update_view()
        return False

    def connect_server(self):
        config = open('config/prd.json')
        properties = json.load(config)

        SERVER_IP = properties['HOST_IP']
        SERVER_PORT = properties['HOST_PORT']

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((SERVER_IP, SERVER_PORT))
        except socket.error as msg:
            print("Connection error:{msg}".format(msg=msg))
            return False

        return s

    def listen_server_payload(self, s):
        print("開始監聽server")
        while True:
            payload = s.recv(1024)
            split = payload.decode().split('~')
            payload = "{last_payload}~".format(last_payload=split[len(split)-2])

            if len(payload) == 0:  # connection closed
                s.close()
                print('server closed connection.')
                break

            self.handle_receive_payload(payload)

    def handle_receive_payload(self, payload):
        header = payload[0:2]

        # 房間清單
        if header == Payload.RoomListHeader:
            print("進入大廳")
            self.scene = SceneLobby
            room_list = parse_room_list(payload)
            self.lobby.update_rooms_data(room_list)

        # 房間內部細節
        elif header == Payload.RoomDetailHeader:
            print("進入房間")
            self.scene = SceneRoom
            room_internal_model = parse_player_list(payload)
            self.room.update_players(room_internal_model)

        # 對手投降
        elif header == Payload.GiveUpBattleHeader:
            # 顯示對手投降
            print("對手投降")
            self.scene = SceneRoom

            pass

        # 自己投降
        elif header == Payload.GiveUpByMyselfHeader:
            # 自己投降
            print("自己投降")
            self.scene = SceneRoom

        # 成功離開大廳通知
        elif header == Payload.LeaveLobby:
            print("成功離開大廳")
            self.scene = SceneHome

        # 戰鬥準備開始
        elif header == Payload.StartBattleHeader:
            self.scene = SceneCountDownBattle

            # 填入戰鬥房間id
            self.battle.room_id = self.room.players_data.room_id

        # 戰鬥過程封包
        elif header == Payload.BattleSituationHeader:
            self.scene = SceneBattle
            battle_info = parse_battle_info(payload)
            self.battle.update_battle_situation(battle_info)

        # 戰鬥結束通知
        elif header == Payload.BattleOverHeader:
            self.scene = SceneRoom
            # 戰鬥結束提醒
            print("戰鬥結束")
            pass

        elif header == Payload.OnlinePlayerCount:
            # 更新當下大廳人數
            online_player_count = parse_online_player_count(payload)
            self.lobby.online_player_count = int(online_player_count)


def set_player_name(socket_conn, player_name):
    payload = set_player_name_payload_template(player_name)
    socket_conn.send(str.encode(payload))


def show_server_not_work_msg(screen):
    head_font = pygame.font.Font('font/coders_crux.ttf', 25)
    msg1 = str("Server might shut down for some reason -> $$$")
    screen.blit(head_font.render(msg1, True, (186, 2, 2)), (180, 540))
    msg2 = str("Please contact author Shawn.")
    screen.blit(head_font.render(msg2, True, (186, 2, 2)), (270, 560))
    pygame.display.update()


def heart_beat_job(socket_conn):
    while True:
        socket_conn.send(str.encode("HB~"))
        time.sleep(3)

