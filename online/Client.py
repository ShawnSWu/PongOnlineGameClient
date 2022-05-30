import threading
import socket

import pygame

from online.payload import Payload
from online.payload.Payload import parse_room_list, parse_player_list, parse_battle_info
from view.BattleView import BattleView
from view.LobbyView import LobbyView
from view.RoomView import RoomView

SceneLobby = 'LOBBY'
SceneRoom = 'ROOM'
SceneBattle = 'BATTLE'

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

        self.lobby = LobbyView(self.screen, socket_conn)
        self.room = RoomView(self.screen, socket_conn)
        self.battle = BattleView(self.screen, socket_conn)

        # 監聽Server回應
        listen_server_thread = threading.Thread(target=self.listen_server_payload, args=(socket_conn,))
        listen_server_thread.start()

        clock = pygame.time.Clock()
        # Lobby Loop
        while True:
            clock.tick(30)

            if self.scene == SceneLobby:
                self.lobby.listen_player_operation()
                self.lobby.draw()

            elif self.scene == SceneRoom:
                self.room.listen_player_operation()
                self.room.draw()

            elif self.scene == SceneBattle:
                self.battle.listen_player_operation()
                self.battle.draw()

            self.lobby.screen_update_view()

    def connect_server(self):
        SERVER_IP = "127.0.0.1"
        SERVER_PORT = 4321
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        return s

    def listen_server_payload(self, s):
        print("開始監聽server")
        while True:
            payload = s.recv(1024)

            if len(payload) == 0:  # connection closed
                s.close()
                print('server closed connection.')
                break

            self.handle_receive_payload(payload.decode())

    def handle_receive_payload(self, payload):
        header = payload[0:2]

        # 房間清單
        if header == Payload.RoomListHeader:
            self.scene = SceneLobby
            room_list = parse_room_list(payload)
            self.lobby.update_rooms_data(room_list)

        # 房間內部細節
        elif header == Payload.RoomDetailHeader:
            self.scene = SceneRoom
            room_internal_model = parse_player_list(payload)
            self.room.update_players(room_internal_model)

        # 對手投降
        elif header == Payload.GiveUpBattleHeader:
            # 顯示對手投降
            pass

        # 戰鬥準備開始
        elif header == Payload.StartBattleHeader:
            self.scene = SceneBattle

            # 填入戰鬥房間id
            self.battle.room_id = self.room.players_data.room_id

        # 戰鬥過程封包
        elif header == Payload.BattleSituationHeader:
            battle_info = parse_battle_info(payload)
            self.battle.update_battle_situation(battle_info)
