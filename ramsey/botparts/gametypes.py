import enum

class Player(enum.Enum):
    p1 = 1
    p2 = 2
    
    def other(self):
        return Player.p1 if self == Player.p2 else Player.p2
    
    def set_color(self, color):
        self.color = color
        # not sure this is really necessary, but:
        return color