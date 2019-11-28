import matplotlib
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from snake.main import SnakeAPP
from snake import utils


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
        plt.cla()
        x, y1, y2 = PlotScreen.resize_plot_data()
        plt.plot(x, y1, label='Fitness')
        plt.plot(x, y2, label='Avg. Fitness')
        plt.xlabel('Generation')
        plt.legend()
        Screen.plot_widget.grid(row=0, column=0)
        Screen.plot_canvas.draw()

    @staticmethod
    def resize_plot_data():
        plot_data = utils.get_plot_data()
        x, y1, y2 = plot_data
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

