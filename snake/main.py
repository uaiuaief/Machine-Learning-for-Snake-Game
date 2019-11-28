import random
from tkinter import mainloop, CENTER, NW


class SnakeAPP:

    config = {
        "TICK": 100,

        "SNAKE_BODY_COLOR": 'green',
        "SNAKE_HEAD_COLOR": 'lime green',

        "BACKGROUND_COLOR": 'black',
        "FOOD_COLOR": 'red',

        "GRID_WIDTH_IN_SQMS": 20,
        "GRID_HEIGHT_IN_SQMS": 20,
        "GRID_SQM_SIZE": 30,
        "SCREEN_TITLE": 'Snake Game',

        # Starting Screen:
        "BUTTON_TEXT_FONT": 'verdana',
        "BUTTON_TEXT_ANCHOR": 'nw',

        "PLAY_BUTTON_TEXT_COORDINATES": (77, 215),
        # "PLAY_BUTTON_TEXT_COORDINATES": (100, 200),
        "PLAY_BUTTON_TEXT": "Normal Mode",
        "PLAY_BUTTON_TEXT_COLOR": "gray60",
        "PLAY_BUTTON_TEXT_SIZE": 50,
        "PLAY_BUTTON_ACTIVE_FILL": 'white',

        "AI_BUTTON_TEXT_COLOR": "gray60",
        "AI_BUTTON_TEXT_SIZE": 50,
        "AI_BUTTON_TEXT_COORDINATES": (158, 315),
        "AI_BUTTON_TEXT": 'AI Mode',
        "AI_BUTTON_ACTIVE_FILL": 'white',

        "SEE_FITTEST_BUTTON_TEXT_COLOR": "SkyBlue4",
        "SEE_FITTEST_BUTTON_TEXT_SIZE": 12,
        "SEE_FITTEST_BUTTON_TEXT_COORDINATES": (472, 10),
        "SEE_FITTEST_BUTTON_TEXT": 'Watch Best AI',
        "SEE_FITTEST_BUTTON_ACTIVE_FILL": 'SkyBlue2',

        "PLOT_DISPLAY_BUTTON_TEXT_COLOR": "SkyBlue4",
        "PLOT_DISPLAY_BUTTON_TEXT_SIZE": 12,
        "PLOT_DISPLAY_BUTTON_TEXT_COORDINATES": (388, 10),
        "PLOT_DISPLAY_BUTTON_TEXT": 'Charts  |',
        "PLOT_DISPLAY_BUTTON_ACTIVE_FILL": 'SkyBlue2',

        # AI Screen:

        "MENU_BUTTON_TEXT_FONT": 'verdana',
        "MENU_BUTTON_TEXT_COORDINATES": (530, 10),
        "MENU_BUTTON_TEXT": "Menu",
        "MENU_BUTTON_TEXT_COLOR": "SkyBlue4",
        "MENU_BUTTON_TEXT_SIZE": 18,
        "MENU_BUTTON_ACTIVE_FILL": 'SkyBlue2',

        "TICK_BUTTON_TEXT_FONT": 'arial',
        "TICK_BUTTON_TEXT_COORDINATES": (150, 10),
        "TICK_BUTTON_TEXT": "Tick",
        "TICK_BUTTON_TEXT_COLOR": "gray80",
        "TICK_BUTTON_TEXT_SIZE": 8,

        "GRAPHICS_BUTTON_TEXT_FONT": 'arial',
        "GRAPHICS_BUTTON_TEXT_COORDINATES": (200, 10),
        "GRAPHICS_BUTTON_TEXT": "Graphics",
        "GRAPHICS_BUTTON_TEXT_COLOR": "gray80",
        "GRAPHICS_BUTTON_TEXT_SIZE": 8,

        # Score:
        # HIGH SCORE
        "HIGH_SCORE_TEXT_FONT": 'arial',
        "HIGH_SCORE_TEXT_ANCHOR": NW,
        "HIGH_SCORE_LABEL_TEXT_COLOR": "gray80",
        "HIGH_SCORE_LABEL_TEXT_SIZE": 10,
        "HIGH_SCORE_LABEL_TEXT_COORDINATES": (10, 10),
        "HIGH_SCORE_LABEL_TEXT": None,
        "HIGH_SCORE_LABEL_ACTIVE_FILL": None,
        # CURRENT SCORE
        "CURRENT_SCORE_TEXT_FONT": 'arial',
        "CURRENT_SCORE_TEXT_ANCHOR": CENTER,
        "CURRENT_SCORE_LABEL_TEXT_COLOR": "gray3",
        "CURRENT_SCORE_LABEL_TEXT_SIZE": 300,
        "CURRENT_SCORE_LABEL_TEXT_COORDINATES": None,
        "CURRENT_SCORE_LABEL_TEXT": None,
        "CURRENT_SCORE_LABEL_ACTIVE_FILL": None,

        # AI Configurations:
        "WATCHING_TICK": 0.03,
        "AI_TICK": 0.0,
        "MUTATION_RATE": random.randint(20, 500)/100,
        "MUTATION_THRESHOLD": 48,
        "LIFE_SPAN": 45,
        "POPULATION_SIZE": 120,
        "APPLE_AMOUNT_TO_INCREASE": 45,

        # PLOT Configurations:
        'PLOT_X_AXIS_AMOUNT': 70,
        "PLOT_SIZE": (6.04, 5),
    }

    @staticmethod
    def run():
        from snake.view import View
        view = View()
        view.goto_starting_screen()
        mainloop()


