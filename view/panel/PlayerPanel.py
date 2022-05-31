class PlayerPanel:
    def __init__(self, x, y, player_name, name_text_location, description_text_location):
        self.x = x
        self.y = y
        self.player_name = player_name
        self.description_text = 'Lorem ipsum dolor sit amet.'
        self.name_text_location = name_text_location
        self.description_text_location = description_text_location
        self.bg_color = (0, 174, 174)
        self.width = 337
        self.height = 330
        self.ready_status = 0
        self.display = False
