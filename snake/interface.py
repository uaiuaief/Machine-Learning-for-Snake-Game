from snake.screens import Screen, StartingScreen, GameScreen, AIScreen, PlotScreen, FittestDisplayScreen
from snake.draw import Snake, Grid
from tkinter import Frame, Button, StringVar
from snake.main import SnakeAPP


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
                                      width=19, font=('arial', 12, 'normal'), command=self.graphics_IO)
        self.tick_button = Button(self.top_frame, text="Tick", bg='SlateGray1', activebackground='SlateGray2',
                                  width=19, font=('arial', 12, 'normal'), command=self.tick_IO)
        self.close_button = Button(self.top_frame, textvariable=self.close_button_text, bg='SlateGray1',
                                   width=19, font=('arial', 12, 'normal'), activebackground='SlateGray2',
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

