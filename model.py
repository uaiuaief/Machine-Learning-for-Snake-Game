import numpy
import random
from snake.snake_main import SnakeAPP
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib


class Screen:
    frame = Tk()
    frame.title(SnakeAPP.config['SCREEN_TITLE'])
    frame.resizable(width=False, height=False)

    canvas_width = SnakeAPP.config['GRID_WIDTH_IN_SQMS'] * SnakeAPP.config['GRID_SQM_SIZE']
    canvas_height = SnakeAPP.config['GRID_HEIGHT_IN_SQMS'] * SnakeAPP.config['GRID_SQM_SIZE']

    canvas = Canvas(frame, width=canvas_width, height=canvas_height, bg=SnakeAPP.config['BACKGROUND_COLOR'])

    # Matplotlib
    matplotlib.use('TkAgg')
    fig = plt.figure(figsize=(SnakeAPP.config['PLOT_SIZE']))

    # Special type of "canvas" to allow for matplotlib graphing
    plot_canvas = FigureCanvasTkAgg(fig, master=frame)
    plot_widget = plot_canvas.get_tk_widget()

    frame.protocol('WM_DELETE_WINDOW', lambda: Screen.on_close())

    @staticmethod
    def on_close():
        plt.close()
        Screen.frame.destroy()


class FittestDisplayScreen(Screen):
    close = False

    @classmethod
    def set_close(cls, event=None):
        cls.close = True

    @staticmethod
    def display_text(text):
        Screen.canvas.create_text(SnakeAPP.config['HIGH_SCORE_LABEL_TEXT_COORDINATES'],
                                  text=text, fill=SnakeAPP.config["HIGH_SCORE_LABEL_TEXT_COLOR"],
                                  font=(SnakeAPP.config["HIGH_SCORE_TEXT_FONT"],
                                        SnakeAPP.config["HIGH_SCORE_LABEL_TEXT_SIZE"]),
                                  anchor=SnakeAPP.config["HIGH_SCORE_TEXT_ANCHOR"])

    @staticmethod
    def display_current_score(current_score=''):
        Screen.canvas.create_text(Screen.canvas_width / 2, Screen.canvas_height / 2,
                                  text=current_score, fill=SnakeAPP.config["CURRENT_SCORE_LABEL_TEXT_COLOR"],
                                  font=(SnakeAPP.config["CURRENT_SCORE_TEXT_FONT"],
                                        SnakeAPP.config["CURRENT_SCORE_LABEL_TEXT_SIZE"]),
                                  anchor=SnakeAPP.config["CURRENT_SCORE_TEXT_ANCHOR"])


class PlotScreen(Screen):

    @staticmethod
    def show():
        # plt.gca().clear()
        plt.cla()
        x, y1, y2 = PlotScreen.resize_plot_data()
        plt.plot(x, y1, label='Fitness')
        plt.plot(x, y2, label='Avg. Fitness')
        plt.xlabel('Generation')
        plt.legend()
        Screen.plot_widget.grid(row=0, column=0)
        Screen.plot_canvas.draw()


    @staticmethod
    def get_plot_data():
        try:
            with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\plotgraph.txt', 'r') as file:
                data = file.read()
                if data != '':
                    # CREATE GENERATION AXIS
                    first_pattern = re.compile(r'\'Generation\': \d+')
                    matches = first_pattern.finditer(data)
                    string_array = []
                    for m in matches:
                        result = m.group(0)
                        string_array.append(m.group(0))
                        # print(result)

                    x = []
                    second_pattern = re.compile(r'\d+')
                    for string in string_array:
                        matches = second_pattern.finditer(string)
                        for m in matches:
                            result = m.group(0)
                            x.append(int(result))
                            # print(result)

                    # CREATE FITNESS AXIS
                    first_pattern = re.compile(r'\'Fitness\': \d+')
                    matches = first_pattern.finditer(data)
                    string_array = []
                    for m in matches:
                        result = m.group(0)
                        string_array.append(m.group(0))
                        # print(result)

                    y1 = []
                    second_pattern = re.compile(r'\d+')
                    for string in string_array:
                        matches = second_pattern.finditer(string)
                        for m in matches:
                            result = m.group(0)
                            y1.append(int(result))
                            # print(result)

                    # CREATE AVERAGE FITNESS AXIS
                    first_pattern = re.compile(r'Avg. Fitness\': \d+')
                    matches = first_pattern.finditer(data)
                    string_array = []
                    for m in matches:
                        result = m.group(0)
                        string_array.append(m.group(0))
                        # print(result)

                    y2 = []
                    second_pattern = re.compile(r'\d+')
                    for string in string_array:
                        matches = second_pattern.finditer(string)
                        for m in matches:
                            result = m.group(0)
                            y2.append(int(result))

                    return [x, y1, y2]
                else:
                    return [[], [], []]

        except FileNotFoundError:
            print("File Not Found")

    @staticmethod
    def resize_plot_data():
        x, y1, y2 = PlotScreen.get_plot_data()
        interval = len(x)//SnakeAPP.config['PLOT_X_AXIS_AMOUNT']

        if len(x) <= SnakeAPP.config['PLOT_X_AXIS_AMOUNT']:
            return x, y1, y2
        else:
            h, v1, v2 = [], [], []
            for a, b, c in zip(x, y1, y2):
                if a % interval == 0:
                    h.append(a)
                    v1.append(b)
                    v2.append(c)

            return h, v1, v2


class AIScreen(Screen):
    graphics = True
    graphics_text = 'On'
    ai_tick = SnakeAPP.config['AI_TICK']

    @staticmethod
    def display_high_score(high_score):
        Screen.canvas.create_text(SnakeAPP.config['HIGH_SCORE_LABEL_TEXT_COORDINATES'],
                                  text=high_score, fill=SnakeAPP.config["HIGH_SCORE_LABEL_TEXT_COLOR"],
                                  font=(SnakeAPP.config["HIGH_SCORE_TEXT_FONT"],
                                        SnakeAPP.config["HIGH_SCORE_LABEL_TEXT_SIZE"]),
                                  anchor=SnakeAPP.config["HIGH_SCORE_TEXT_ANCHOR"])


class GameScreen(Screen):
    @staticmethod
    def display_high_score(high_score):
        Screen.canvas.create_text(SnakeAPP.config['HIGH_SCORE_LABEL_TEXT_COORDINATES'],
                                  text=high_score, fill=SnakeAPP.config["HIGH_SCORE_LABEL_TEXT_COLOR"],
                                  font=(SnakeAPP.config["HIGH_SCORE_TEXT_FONT"],
                                        SnakeAPP.config["HIGH_SCORE_LABEL_TEXT_SIZE"]),
                                  anchor=SnakeAPP.config["HIGH_SCORE_TEXT_ANCHOR"])

    @staticmethod
    def display_current_score(current_score=''):
        Screen.canvas.create_text(Screen.canvas_width/2, Screen.canvas_height/2,
                                  text=current_score, fill=SnakeAPP.config["CURRENT_SCORE_LABEL_TEXT_COLOR"],
                                  font=(SnakeAPP.config["CURRENT_SCORE_TEXT_FONT"],
                                        SnakeAPP.config["CURRENT_SCORE_LABEL_TEXT_SIZE"]),
                                  anchor=SnakeAPP.config["CURRENT_SCORE_TEXT_ANCHOR"])


class StartingScreen(Screen):
    play_button = None
    ai_button = None
    fittest_display_button = None
    plot_display_button = None

    @classmethod
    def create_buttons(cls):
        cls.play_button = Screen.canvas.create_text(SnakeAPP.config['PLAY_BUTTON_TEXT_COORDINATES'],
                                                    font=(SnakeAPP.config['BUTTON_TEXT_FONT'],
                                                          SnakeAPP.config['PLAY_BUTTON_TEXT_SIZE']),
                                                    text=SnakeAPP.config['PLAY_BUTTON_TEXT'],
                                                    fill=SnakeAPP.config['PLAY_BUTTON_TEXT_COLOR'],
                                                    activefill=SnakeAPP.config['PLAY_BUTTON_ACTIVE_FILL'],
                                                    anchor=SnakeAPP.config['BUTTON_TEXT_ANCHOR']
                                                    )

        cls.ai_button = Screen.canvas.create_text(SnakeAPP.config['AI_BUTTON_TEXT_COORDINATES'],
                                                  font=(SnakeAPP.config['BUTTON_TEXT_FONT'],
                                                        SnakeAPP.config['AI_BUTTON_TEXT_SIZE']),
                                                  text=SnakeAPP.config['AI_BUTTON_TEXT'],
                                                  fill=SnakeAPP.config['AI_BUTTON_TEXT_COLOR'],
                                                  activefill=SnakeAPP.config['AI_BUTTON_ACTIVE_FILL'],
                                                  anchor=SnakeAPP.config['BUTTON_TEXT_ANCHOR']
                                                  )

        cls.fittest_display_button = Screen.canvas.create_text(SnakeAPP.config['SEE_FITTEST_BUTTON_TEXT_COORDINATES'],
                                                               font=(SnakeAPP.config['BUTTON_TEXT_FONT'],
                                                                     SnakeAPP.config['SEE_FITTEST_BUTTON_TEXT_SIZE']),
                                                               text=SnakeAPP.config['SEE_FITTEST_BUTTON_TEXT'],
                                                               fill=SnakeAPP.config['SEE_FITTEST_BUTTON_TEXT_COLOR'],
                                                               activefill=SnakeAPP.config['SEE_FITTEST_BUTTON_ACTIVE_FILL'],
                                                               anchor=SnakeAPP.config['BUTTON_TEXT_ANCHOR']
                                                  )
        cls.plot_display_button = Screen.canvas.create_text(SnakeAPP.config['PLOT_DISPLAY_BUTTON_TEXT_COORDINATES'],
                                                               font=(SnakeAPP.config['BUTTON_TEXT_FONT'],
                                                                     SnakeAPP.config['PLOT_DISPLAY_BUTTON_TEXT_SIZE']),
                                                               text=SnakeAPP.config['PLOT_DISPLAY_BUTTON_TEXT'],
                                                               fill=SnakeAPP.config['PLOT_DISPLAY_BUTTON_TEXT_COLOR'],
                                                               activefill=SnakeAPP.config[
                                                                   'PLOT_DISPLAY_BUTTON_ACTIVE_FILL'],
                                                               anchor=SnakeAPP.config['BUTTON_TEXT_ANCHOR']
                                                            )


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


# User Interface:
class UI:
    ai_tick = SnakeAPP.config['AI_TICK']
    watching_tick = SnakeAPP.config['WATCHING_TICK']
    tick = SnakeAPP.config['TICK']
    current_screen = None
    frame = Screen.frame
    canvas = Screen.canvas

    starting_screen = StartingScreen
    game_screen = GameScreen
    ai_screen = AIScreen
    plot_screen = PlotScreen
    fittest_display_screen = FittestDisplayScreen

    grid = Grid()
    snake = Snake(grid=grid)
    grid.add_snake(snake)
    grid.generate_food()
    graphics = True

    def __init__(self):
        self.close = False
        self.close_button_text = StringVar()
        self.close_button_text.set('Menu')

        self.top_frame = Frame(self.frame)
        self.graphics_button = Button(self.top_frame, text="Graphics", bg='SlateGray1', activebackground='SlateGray2',
                                      width=21, font=('arial', 12, 'normal'), command=self.graphics_IO)
        self.tick_button = Button(self.top_frame, text="Tick", bg='SlateGray1', activebackground='SlateGray2',
                                  width=21, font=('arial', 12, 'normal'), command=self.tick_IO)
        self.close_button = Button(self.top_frame, textvariable=self.close_button_text, bg='SlateGray1',
                                   width=21, font=('arial', 12, 'normal'), activebackground='SlateGray2',
                                   command=self.save_and_close)
        self.graphics_button.grid(row=0, column=0)
        self.tick_button.grid(row=0, column=1)
        self.close_button.grid(row=0, column=2)


    def graphics_IO(self):
        self.graphics = not self.graphics
        if self.ai_tick == SnakeAPP.config['WATCHING_TICK']:
            self.ai_tick = SnakeAPP.config['AI_TICK']

    def tick_IO(self):
        if self.ai_tick == SnakeAPP.config['AI_TICK'] and self.graphics:
            self.ai_tick = SnakeAPP.config['WATCHING_TICK']
        else:
            self.ai_tick = SnakeAPP.config['AI_TICK']

    def save_and_close(self):
        self.close = True
        self.close_button_text.set('Waiting...')

    def draw_canvas(self):
        self.canvas.create_rectangle(self.snake.head.get_coord(), fill=SnakeAPP.config['SNAKE_HEAD_COLOR'])
        self.canvas.create_rectangle(self.grid.food.get_coord(), fill=SnakeAPP.config['FOOD_COLOR'])

        for part in self.snake.body:
            if part != self.snake.head:
                self.canvas.create_rectangle(part.get_coord(), fill=SnakeAPP.config['SNAKE_BODY_COLOR'])


''' __________________________________________________________________ '''
''' AI STUFF'''


class Gene:
    def __init__(self, parent_data=None):
        self.data = []
        if parent_data is None:
            self.generate()
        else:
            self.data = parent_data

    def generate(self):
        for _ in range(12):
            # self.data.append(random.randint(-2,2))
            self.data.append(numpy.random.standard_normal())

    def mutate(self):
        data = []
        for each in self.data:
            if random.choice([i for i in range(SnakeAPP.config['MUTATION_THRESHOLD'])]) == 0:
                # data.append(each*numpy.random.standard_normal())
                # data.append(each*random.choice([-2, 2, -0.5, 0.5]))
                data.append(each*random.choice([1,-1]))
            else:
                data.append(each)
            # data.append(each * MUTATION_RATE)

        self.data = data


# Snake AI Input Layer
class InputLayer:
    def __init__(self, snake):
        self.snake = snake
        self.food = self.snake.grid.food

    def get_input_matrix(self):
        input_matrix = [
            self.up_food_distance(),
            self.down_food_distance(),
            self.left_food_distance(),
            self.right_food_distance(),

            self.up_tail_distance(),
            self.down_tail_distance(),
            self.left_tail_distance(),
            self.right_tail_distance(),

            self.up_wall_distance(),
            self.down_wall_distance(),
            self.left_wall_distance(),
            self.right_wall_distance(),
        ]
        adjusted_matrix = []

        for each in input_matrix:
            if each is None:
                each = 0
            adjusted_matrix.append(each)

        input_matrix = adjusted_matrix

        return input_matrix

    ''' Sensing functions:
        Sense FOOD                              '''
    def is_food_to_the_right(self):
        if self.snake.head.y1 == self.food.y1 and self.snake.head.x1 < self.food.x1:
            return True
        else:
            return False

    def is_food_to_the_left(self):
        if self.snake.head.y1 == self.food.y1 and self.snake.head.x1 > self.food.x1:
            return True
        else:
            return False

    def is_food_upwards(self):
        if self.snake.head.x1 == self.food.x1 and self.snake.head.y1 > self.food.y1:
            return True
        else:
            return False

    def is_food_downwards(self):
        if self.snake.head.x1 == self.food.x1 and self.snake.head.y1 < self.food.y1:
            return True
        else:
            return False

    '''Distance from objects: 
            FOOD:               '''
    def up_food_distance(self):
        if self.is_food_upwards():
            distance = self.snake.head.y1 - self.food.y1
            return distance

    def down_food_distance(self):
        if self.is_food_downwards():
            distance = self.food.y1 - self.snake.head.y1
            return distance

    def left_food_distance(self):
        if self.is_food_to_the_left():
            distance = self.snake.head.x1 - self.food.x1
            return distance

    def right_food_distance(self):
        if self.is_food_to_the_right():
            distance = self.food.x1 - self.snake.head.x1
            return distance

    '''     TAIL:               '''
    def up_tail_distance(self):
        for member in self.snake.body:
            if member != self.snake.head and self.snake.head.x1 == member.x1 and self.snake.head.y1 > member.y1:
                distance = self.snake.head.y1 - member.y1
                return distance

    def down_tail_distance(self):
        for member in self.snake.body:
            if member != self.snake.head and self.snake.head.x1 == member.x1 and self.snake.head.y1 < member.y1:
                distance = member.y1 - self.snake.head.y1
                return distance

    def right_tail_distance(self):
        for member in self.snake.body:
            if member != self.snake.head and self.snake.head.y1 == member.y1 and self.snake.head.x1 < member.x1:
                distance = member.x1 - self.snake.head.x1
                return distance

    def left_tail_distance(self):
        for member in self.snake.body:
            if member != self.snake.head and self.snake.head.y1 == member.y1 and self.snake.head.x1 > member.x1:
                distance = self.snake.head.x1 - member.x1
                return distance

    '''     WALL:               '''
    def up_wall_distance(self):
        distance = self.snake.head.y1 - 0
        return distance

    def down_wall_distance(self):
        distance = self.snake.grid.height - self.snake.head.y1
        return distance

    def left_wall_distance(self):
        distance = self.snake.head.x1 - 0
        return distance

    def right_wall_distance(self):
        distance = self.snake.grid.width - self.snake.head.x1
        return distance


# Snake AI Hidden Layer
class HiddenLayer:
    def __init__(self, snake, parent_data=None):
        self.snake = snake
        if parent_data is None:
            self.genes = [Gene() for _ in range(4)]
        else:
            self.genes = []
            for each in parent_data:
                self.genes.append(Gene(each))

        self.output_matrix = []

    def process_data(self, input_layer_data):
        output_matrix = []
        for each_gene in self.genes:
            row = []
            for each_input, data in zip(input_layer_data, each_gene.data):
                processed_data = (each_input*data)+1
                row.append(self.activation(processed_data))

            output_matrix.append(row)

        self.output_matrix = output_matrix

    @staticmethod
    def activation(x):
        if x < 0:
            return 0
        elif x >= 0:
            return 1

    def get_processed_data(self, input_layer_data):
        self.process_data(input_layer_data=input_layer_data)
        return self.output_matrix

    def mutate(self):
        for each in self.genes:
            each.mutate()

    def get_genetic_information(self):
        information = [gene.data for gene in self.genes]
        return information


# Snake AI Output Layer
class OutputLayer:
    def __init__(self, snake):
        self.snake = snake

        self.output = {
            'up': 0,
            'down': 0,
            'left': 0,
            'right': 0
        }

    def generate_output(self, hidden_layer_data):
        for data, action in zip(hidden_layer_data, self.output):
            self.output[action] = round(sum(data), 2)

    def get_action(self, hidden_layer_data):
        self.generate_output(hidden_layer_data=hidden_layer_data)
        return self.keywithmaxval(self.output)

    @staticmethod
    def keywithmaxval(d):
        """ a) create a list of the dict's keys and values;
            b) return the key with the max value"""
        v = list(d.values())
        k = list(d.keys())

        return k[v.index(max(v))]


class NeuralNetwork:
    def __init__(self, snake, hidden_layer_data=None):
        self.food_position = []
        self.snake = snake
        self.apple_increase = SnakeAPP.config['APPLE_AMOUNT_TO_INCREASE']
        self.fitness = 0
        self.lifespan = SnakeAPP.config['LIFE_SPAN']
        self.input_layer = InputLayer(snake=self.snake)

        if hidden_layer_data is None:
            self.hidden_layer = HiddenLayer(snake=self.snake)
        else:
            self.hidden_layer = HiddenLayer(snake=self.snake, parent_data=hidden_layer_data)

        self.output_layer = OutputLayer(snake=self.snake)

    def make_decision(self):
        input_matrix = self.input_layer.get_input_matrix()
        hidden_matrix = self.hidden_layer.get_processed_data(input_layer_data=input_matrix)
        action = self.output_layer.get_action(hidden_layer_data=hidden_matrix)
        return action

    def mutate(self):
        self.hidden_layer.mutate()

    def increase_fitness(self, amount=10):
        self.fitness += amount

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, amount):
        self.fitness = amount

    def reset_lifespan(self):
        self.lifespan = SnakeAPP.config['LIFE_SPAN']

    def decrease_lifespan(self):
        self.lifespan -= 1
        if self.lifespan == 0:
            self.snake.is_alive = False

    def get_child(self):
        hidden_layer_data = self.hidden_layer.get_genetic_information()

        child = NeuralNetwork(snake=self.snake, hidden_layer_data=hidden_layer_data)
        child.mutate()

        return child


class Population:
    plot_data = None
    generation = 0
    fittest = None

    def __init__(self, snake, next_generation=None, load=None):

        self.snake = snake
        self.fittest = None

        if load is None:
            if next_generation is None:
                self.members = [NeuralNetwork(self.snake) for _ in range(SnakeAPP.config['POPULATION_SIZE'])]
            else:
                self.members = next_generation
        else:
            self.members = [NeuralNetwork(self.snake,
                                          hidden_layer_data=load) for _ in range(SnakeAPP.config['POPULATION_SIZE'])]

    def get_fittest(self):
        for each in self.members:
            if self.fittest is None:
                self.fittest = each
            elif each.get_fitness() > self.fittest.get_fitness():
                self.fittest = each

        if Population.fittest is not None:
            if Population.fittest.get_fitness() < self.fittest.get_fitness():
                Population.fittest = self.fittest

        return self.fittest

    def get_average_fitness(self):
        fitness_list = [each.get_fitness() for each in self.members]
        return round(sum(fitness_list)/len(fitness_list))

    def get_next_generation(self):
        fittest = self.get_fittest()
        if True:
            Population.plot_data = ({'Fitness': fittest.get_fitness(), 'Generation': self.generation, 'Avg. Fitness': self.get_average_fitness()})
        self.save_genetic_data()
        self.generation += 1
        print(f'Generation: {self.generation}')

        next_generation = []
        for _ in range(SnakeAPP.config['POPULATION_SIZE']):
            next_generation.append(fittest.get_child())

        self.members = next_generation
        fittest.set_fitness(0)
        # if Population.fittest is not None:
        #     self.members.append(Population.fittest)

        self.fittest = None

    def save_genetic_data(self):
        # fittest = self.get_fittest()
        fittest = self.fittest
        genetic_data = fittest.hidden_layer.get_genetic_information()

        # Save genetic data:
        if genetic_data != [[]] and genetic_data != []:
            try:
                with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\genetic data.txt', 'w') as file:
                    file.write(str(genetic_data))
            except FileNotFoundError:
                pass
            except AttributeError:
                print("No data to be saved")
        else:
            print("Data Not Saved")

        # Save generation number:
        if self.generation != '':
            try:
                with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\generation.txt', 'w') as file:
                    file.write(str(self.generation))
            except FileNotFoundError:
                pass

        # Save food coordinates:
        if fittest.food_position != '':
            try:
                with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\food_coord.txt', 'w') as file:
                    file.write(str(fittest.food_position))
            except FileNotFoundError:
                pass

        # Save fittest fitness and generation number:
        if Population.plot_data != '':
            try:
                with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\plotgraph.txt', 'a') as file:
                    to_write = Population.plot_data
                    file.write(str(to_write))
            except FileNotFoundError:
                print('file not found')