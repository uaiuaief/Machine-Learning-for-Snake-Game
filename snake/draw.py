import random
from snake.main import SnakeAPP


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


# Grid where the snake will move
class Grid:
    def __init__(self):
        self.score = 0
        self.snake = None
        self.sqm_size = SnakeAPP.config['GRID_SQM_SIZE']

        self.x_sqms = SnakeAPP.config['GRID_WIDTH_IN_SQMS']
        self.y_sqms = SnakeAPP.config['GRID_HEIGHT_IN_SQMS']

        self.width = SnakeAPP.config['GRID_WIDTH_IN_SQMS'] * self.sqm_size
        self.height = SnakeAPP.config['GRID_HEIGHT_IN_SQMS'] * self.sqm_size

        self.food = Square()

    def get_sqm_size(self):
        return self.sqm_size

    def add_snake(self, snake):
        self.snake = snake

    def generate_food(self):
        bol = True
        while bol == True:
            rx = random.randint(0, self.x_sqms-1)
            rx = rx*self.sqm_size
            ry = random.randint(0, self.y_sqms-1)
            ry = ry*self.sqm_size

            coord = rx,ry,rx+self.sqm_size, ry+self.sqm_size
            self.food.set_coord(coord)

            for member in self.snake.body:
                if self.food.get_coord() == member.get_coord():
                    bol = True
                    break
                else:
                    bol = False


# Snake:
class Snake:
    def __init__(self, grid):
        self.is_control_chosen = False
        self.is_alive = True

        self.is_apple_eaten = False

        self.og_grid = grid
        self.grid = grid
        self.size = grid.get_sqm_size()

        self.head = Square()
        self.head.x1 = (grid.x_sqms/2) * self.size
        self.head.x2 = self.head.x1 + self.size
        self.head.y1 = grid.y_sqms/2 * self.size
        self.head.y2 = self.head.y1 + self.size

        self.body = [self.head, Square(), Square()]

        self.velx = 0
        self.vely = 0

        self.prev_coord = self.head.get_coord()
        self.decision = None

    def reset(self, grid):
        self.is_control_chosen = False
        self.is_alive = True

        self.grid = grid
        self.size = self.grid.get_sqm_size()

        self.head = Square()
        self.head.x1 = (self.grid.x_sqms / 2) * self.size
        self.head.x2 = self.head.x1 + self.size

        self.head.y1 = self.grid.y_sqms / 2 * self.size
        self.head.y2 = self.head.y1 + self.size

        self.body = [self.head, Square(), Square()]

        self.velx = 0
        self.vely = 0

        self.prev_coord = self.head.get_coord()

    def move(self):
        # BODY MOVEMENT
        for member in self.body:
            if member == self.head:
                self.prev_coord = member.get_coord()
                continue
            save_coord = member.get_coord()
            member.set_coord(self.prev_coord)
            member.has_moved = True
            self.prev_coord = save_coord

        # END BODY MOVEMENT

        # Horizontal boundaries:
        if self.head.x2 > self.grid.width - (self.grid.get_sqm_size()) and self.velx > 0:
            self.is_alive = False

        elif self.head.x1 <= 0 and self.velx < 0:
            self.is_alive = False

        else:
            self.head.x1 += self.velx
            self.head.x2 = self.head.x1 + self.size

        # Vertical Boundaries:
        if self.head.y1 >= self.grid.height - self.grid.get_sqm_size() and self.vely > 0:
            self.is_alive = False

        elif self.head.y1 <= 0 and self.vely < 0:
            self.is_alive = False

        else:
            self.head.y1 += self.vely
            self.head.y2 = self.head.y1 + self.size

        # CHECK IF IS DEAD
        self.is_dead()

        # EAT FOOD
        if self.head.get_coord() == self.grid.food.get_coord():
            self.add_member()
            self.is_apple_eaten = True
            self.grid.generate_food()

            self.grid.score += 1

        # RESET CHOSEN DIRECTION
        self.is_control_chosen = False

    def up(self):
        if self.vely == 0 and self.is_control_chosen == False:
            self.stop()
            self.vely = -1*self.grid.get_sqm_size()
            self.is_control_chosen = True
        self.head.has_moved = True

    def down(self):
        if self.vely == 0 and self.is_control_chosen == False:
            self.stop()
            self.vely = 1*self.grid.get_sqm_size()
            self.is_control_chosen = True
        self.head.has_moved = True

    def right(self):
        if self.velx == 0 and self.is_control_chosen == False:
            self.stop()
            self.velx = 1*self.grid.get_sqm_size()
            self.is_control_chosen = True
        self.head.has_moved = True

    def left(self):
        if self.velx == 0 and self.is_control_chosen == False:
            self.stop()
            self.velx = -1*self.grid.get_sqm_size()
            self.is_control_chosen = True
        self.head.has_moved = True

    def stop(self):
        self.velx = 0
        self.vely = 0

    def get_coord(self):
        coord = self.x,self.y, self.x2, self.y2
        return coord

    def add_member(self):
        self.body.append(Square())

    def is_dead(self):
        for member in self.body:
            if member != self.head:
                if member.get_coord() == self.head.get_coord() and member.has_moved == True and self.head.has_moved == True:
                    self.is_alive = False

