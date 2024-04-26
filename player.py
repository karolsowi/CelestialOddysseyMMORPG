class Player:
    def __init__(self, skin, pos):
        self.head = Cube(pos, skin)
        self.dirnx = 0
        self.dirny = 0  

    def move(self, key):
        if key == 'left':
            self.dirnx = -1
            self.dirny = 0
        elif key == 'right':
            self.dirnx = 1
            self.dirny = 0
        elif key == 'up':
            self.dirnx = 0
            self.dirny = -1
        elif key == 'down':
            self.dirnx = 0
            self.dirny = 1
        elif key == 'stop':
            self.dirnx = 0
            self.dirny = 0
        self.head.move(self.dirnx, self.dirny)

    def draw(self, surface):
        self.head.draw(surface)

    def get_pos(self):
        return str(self.head.pos)
    

if __name__ == "__main__":
    pass