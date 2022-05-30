class RoomInternalModel:
    def __init__(self, room_id, room_name,
                 player1_id, player1_name, player1_ready_status,
                 player2_id, player2_name, player2_ready_status):
        self.room_id = room_id
        self.room_name = room_name
        self.player1_id = player1_id
        self.player1_name = player1_name
        self.player1_ready_status = player1_ready_status
        self.player2_id = player2_id
        self.player2_name = player2_name
        self.player2_ready_status = player2_ready_status
