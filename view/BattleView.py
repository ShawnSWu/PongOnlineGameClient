import threading

import pygame

from online.payload.Payload import battle_move_up_payload_template, battle_move_down_payload_template, \
    battle_give_up_payload_template
from view.BasicView import BasicView

BALL_RADIUS = 7

lock = threading.Lock()


class PlayerPaddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 150
        self.score = 0


class Ball:
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.image = r'img/ball.png'


class BattleView(BasicView):
    def __init__(self, screen, socket_conn):
        super().__init__(screen)
        self.screen = screen
        self.socket_conn = socket_conn
        self.bg_color = (38, 38, 38)
        w, h = self.get_width_height()
        self.left_paddle = PlayerPaddle(0, h / 2)
        self.room_id = ''
        self.right_paddle = PlayerPaddle(w - 50, h / 2)
        self.ball = Ball(w / 2, h / 2)

    def draw(self):
        lock.acquire()
        self.clear_view(self.bg_color)

        # 中線
        w, h = self.get_width_height()
        self.draw_rect(w / 2, 0, 2, h, (203, 202, 203))

        # hint text
        self.draw_game_text("[z]  -> Surrender", 35, h - 20, 20, bg_color=(94, 94, 94))
        self.draw_game_text("Down -> Move down", 35, h - 35, 20, bg_color=(94, 94, 94))
        self.draw_game_text("Up   -> Move up", 35, h - 50, 20, bg_color=(94, 94, 94))

        left_paddle = self.left_paddle
        self.draw_rect(left_paddle.x, left_paddle.y, left_paddle.width, left_paddle.height, (0, 102, 233))
        self.draw_game_text(left_paddle.score, 195, 15, 150)

        right_paddle = self.right_paddle
        self.draw_rect(right_paddle.x, right_paddle.y, right_paddle.width, right_paddle.height, (122, 30, 11))
        self.draw_game_text(right_paddle.score, 580, 15, 150)

        ball = self.ball
        self.draw_image(ball.image, ball.x, ball.y)

        self.screen_update_view()
        lock.release()

    def update_battle_situation(self, battle_info):
        ball_x = battle_info[0]
        ball_y = battle_info[1]
        player1_x = battle_info[2]
        player1_y = battle_info[3]
        player1_score = battle_info[4]
        player2_x = battle_info[5]
        player2_y = battle_info[6]
        player2_score = battle_info[7]

        self.ball.x = ball_x
        self.ball.y = ball_y
        self.left_paddle.x = player1_x
        self.left_paddle.y = player1_y
        self.left_paddle.score = player1_score
        self.right_paddle.x = player2_x
        self.right_paddle.y = player2_y
        self.right_paddle.score = player2_score

    def draw_battle_ready_start_hint(self):
        self.clear_view(self.bg_color)
        # 戰鬥準備開始提醒
        self.draw_game_text("READY", 280, 284, 150)

    def listen_player_operation(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.handle_operation(event)

    def handle_operation(self, event):
        if event.key == pygame.K_UP:
            self.battle_move_up()
        elif event.key == pygame.K_DOWN:
            self.battle_move_down()
        # 12552 mean 'keyboard z' ,have no idea why pygame.K_z not working
        elif event.key == 12552 or event.key == pygame.K_z:
            self.battle_give_up()

    def battle_move_up(self):
        payload = battle_move_up_payload_template()
        threading.Thread(target=sendByThread, args=(self.socket_conn, payload,)).start()

    def battle_move_down(self):
        payload = battle_move_down_payload_template()
        threading.Thread(target=sendByThread, args=(self.socket_conn, payload,)).start()

    def battle_give_up(self):
        payload = battle_give_up_payload_template(self.room_id)
        threading.Thread(target=sendByThread, args=(self.socket_conn, payload,)).start()


def sendByThread(socket_conn, payload,):
    socket_conn.send(str.encode(payload))
