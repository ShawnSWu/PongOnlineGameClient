from online.model.RoomInternalModel import RoomInternalModel
from online.model.RoomItemModel import RoomItemModel

PlayerNameSetting = "PN"
RoomListHeader = "RL"
LeaveLobby = "LL"
OnlinePlayerCount = "OC"

CreateRoomHeader = "CR"
RoomDetailHeader = "RD"
RoomFullHeader = "RF"
EnterRoomHeader = "ER"
LeaveRoomHeader = "LR"
ReadyStartHeader = "RS"

StartBattleHeader = "SB"
BattleSituationHeader = "BS"
BattleActionHeader = "BA"
BattleOverHeader = "BO"
GiveUpBattleHeader = "GB"
GiveUpByMyselfHeader = "GM"


def _remove_header_and_terminator(payload):
    return payload[2: len(payload) - 1]


def parse_room_list(payload):
    payload = _remove_header_and_terminator(payload)
    single_room_payload = payload.split('&')

    room_list = []

    for sr in single_room_payload:
        single_room = sr.split(',')
        if len(single_room) <= 1:
            break
        room_id = single_room[0]
        room_name = single_room[1]
        create_date = single_room[2]
        player_count = single_room[3]
        room_status = single_room[4]

        room = RoomItemModel(room_id, room_name, create_date, player_count, room_status)
        room_list.append(room)

    return room_list


def parse_player_list(payload):
    payload = _remove_header_and_terminator(payload)
    player_list = payload.split(',')

    room_id = player_list[0]
    room_name = player_list[1]
    player1_id = player_list[2]
    player1_name = player_list[3]
    player1_ready_status = player_list[4]
    player2_id = player_list[5]
    player2_name = player_list[6]
    player2_ready_status = player_list[7]

    return RoomInternalModel(room_id, room_name, player1_id, player1_name, player1_ready_status,
                             player2_id, player2_name, player2_ready_status)


def parse_online_player_count(payload):
    online_player_count = _remove_header_and_terminator(payload)
    return online_player_count


def parse_battle_info(payload):
    payload = _remove_header_and_terminator(payload)
    battle_info = payload.split(',')

    ball_x = int(battle_info[0])
    ball_y = int(battle_info[1])
    player1_x = int(battle_info[2])
    player1_y = int(battle_info[3])
    player1_score = int(battle_info[4])
    player2_x = int(battle_info[5])
    player2_y = int(battle_info[6])
    player2_score = int(battle_info[7])

    return ball_x, ball_y, player1_x, player1_y, player1_score, player2_x, player2_y, player2_score


def parse_battle_over(payload):
    payload = _remove_header_and_terminator(payload)
    over_room_id = payload.split(',')
    pass


def set_player_name_payload_template(player_name):
    return "PN{player_name}~".format(player_name=player_name)

def create_room_payload_template(room_name):
    return "CR{room_name}~".format(room_name=room_name)


def leave_lobby_payload_template():
    return "LL~"


def enter_room_payload_template(room_id):
    return "ER{room_id}~".format(room_id=room_id)


def ready_battle_payload_template(room_id):
    return "RS{room_id}~".format(room_id=room_id)


def leave_room_payload_template(room_id):
    return "LR{room_id}~".format(room_id=room_id)


def battle_move_up_payload_template():
    return "BAU~"


def battle_move_down_payload_template():
    return "BAD~"


def battle_give_up_payload_template(room_id):
    return "GB{room_id},~".format(room_id=room_id)

