import threading

import pygame

from online.payload.Payload import battle_move_up_payload_template, battle_move_down_payload_template
from view.BasicView import BasicView

BALL_RADIUS = 7

lock = threading.Lock()


class Paddle:
    COLOR = (255, 255, 255)
    VEL = 4

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = 10
        self.height = 150
        self.score = 0

    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))


class Ball:
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.color = (196, 88, 88)
        self.radius = radius


class BattleView(BasicView):
    def __init__(self, screen, socket_conn):
        super().__init__(screen)
        self.screen = screen
        self.socket_conn = socket_conn
        self.bg_color = (38, 38, 38)
        w, h = self.get_width_height()
        self.left_paddle = Paddle(0, h/2)
        self.right_paddle = Paddle(w-50, h/2)
        self.ball = Ball(w/2, h/2, BALL_RADIUS)

    def draw(self):
        lock.acquire()
        self.clear_view(self.bg_color)

        left_paddle = self.left_paddle
        self.draw_rect(left_paddle.x, left_paddle.y, left_paddle.width, left_paddle.height, left_paddle.COLOR)

        right_paddle = self.right_paddle
        self.draw_rect(right_paddle.x, right_paddle.y, right_paddle.width, right_paddle.height, right_paddle.COLOR)

        ball = self.ball
        pygame.draw.circle(self.screen, ball.color, (ball.x, ball.y), ball.radius)

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


    def listen_player_operation(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                self.handle_operation(event)

    def handle_operation(self, event):
        if event.key == pygame.K_UP:
            self.battle_move_up()
        elif event.key == pygame.K_DOWN:
            self.battle_move_down()
        elif event.key == pygame.K_RETURN:
            pass

    def battle_move_up(self):
        payload = battle_move_up_payload_template()
        self.socket_conn.send(str.encode(payload))

    def battle_move_down(self):
        payload = battle_move_down_payload_template()
        self.socket_conn.send(str.encode(payload))
