# Square:
class Square:
    def __init__(self):
        # self.size
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

        self.has_moved = False

    def get_coord(self):
        coord = self.x1, self.y1, self.x2, self.y2
        return coord

    def set_coord(self, coord):
        self.x1 = coord[0]
        self.y1 = coord[1]
        self.x2 = coord[2]
        self.y2 = coord[3]