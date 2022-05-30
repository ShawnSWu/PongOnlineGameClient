class RoomItemPanel:
    def __init__(self, x, y, room_name_text, crate_date_text,
                 player_count_text, room_status_text, icon_location):
        self.x = x
        self.y = y
        self.room_name_text = room_name_text
        self.crate_date_text = crate_date_text
        self.player_count_text = player_count_text
        self.room_status_text = room_status_text
        self.icon_location = icon_location
        self.width = 330
        self.height = 116
        self.bg_color = (131, 145, 163)
        self.display = False
