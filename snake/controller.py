import os
import re
from snake.AI import NeuralNetwork, Population
from snake.interface import UI


class Controller:
    def __init__(self, load_population=False):
        self.ui = UI()
        self.neural_network = NeuralNetwork(snake=self.ui.snake)

        if load_population:
            self.population = Population(snake=self.ui.snake, load=self.load_genetic_data())
            self.population.generation = self.load_generation()
        else:
            self.population = Population(snake=self.ui.snake)

    def get_starting_screen(self):
        return self.ui.starting_screen

    def get_game_screen(self):
        return self.ui.game_screen

    def get_ai_screen(self):
        return self.ui.ai_screen

    def get_neural_network(self):
        return self.neural_network

    def load_fittest(self):
        return NeuralNetwork(snake=self.ui.snake, hidden_layer_data=self.load_genetic_data())

    @staticmethod
    def load_genetic_data():
        try:
            with open(os.path.join(os.getcwd(), 'snake/data/genetic_data'), 'r') as file:
                data = file.read()

                if data != '':
                    first_pattern = re.compile(r'\[[^\[\]]*\]')
                    matches = first_pattern.finditer(data)
                    string_arrays = []
                    for m in matches:
                        string_arrays.append(m.group(0))

                    genetic_data = []
                    second_pattern = re.compile(r'-?\d+\.\d+')
                    for each in string_arrays:
                        matches = second_pattern.finditer(each)
                        row = []
                        for m in matches:
                            row.append(float(m.group(0)))
                        genetic_data.append(row)

                    return genetic_data

                else:
                    raise ValueError('File data must be an array')

        except FileNotFoundError:
            print("File Not Found")

    @staticmethod
    def load_generation():
        try:
            with open(os.path.join(os.getcwd(), 'snake/data/generation'), 'r') as file:

                data = file.read()
                if data != '':
                    return int(data)
                else:
                    raise ValueError("Empty File")

        except FileNotFoundError:
            return 0
            print("File Not Found")

    @staticmethod
    def load_food_coord():
        try:
            with open(os.path.join(os.getcwd(), 'snake/data/food_coord'), 'r') as file:
                data = file.read()

                if data != '':
                    first_pattern = re.compile(r'\d+\, \d+\, \d+\, \d+')
                    matches = first_pattern.finditer(data)
                    string_arrays = []
                    for m in matches:
                        # print(m.group(0))
                        string_arrays.append(m.group(0))

                    food_coords = []
                    second_pattern = re.compile(r'\d+')
                    for each in string_arrays:
                        matches = second_pattern.finditer(each)
                        row = []
                        for m in matches:
                            row.append(int(m.group(0)))
                        food_coords.append(tuple(row))

                    return food_coords

                else:
                    raise ValueError('File data must be an array')

        except FileNotFoundError:
            print("File Not Found")
            return []


class UserControl:
    def __init__(self, ui):
        self.ui = ui
        self.keys = {
                    "U": False,
                    "D": False,
                    "L": False,
                    "R": False
                }

    def up(self, event):
        self.keys["U"] = True

    def noup(self, event):
        self.keys["U"] = False

    def down(self, event):
        self.keys["D"] = True

    def nodown(self, event):
        self.keys["D"] = False

    def left(self, event):
        self.keys["L"] = True

    def noleft(self, event):
        self.keys["L"] = False

    def right(self, event):
        self.keys["R"] = True

    def noright(self, event):
        self.keys["R"] = False

    def no_others(self):
        self.keys["U"] = False
        self.keys["D"] = False
        self.keys["L"] = False
        self.keys["R"] = False

    def move_snake(self):
        if self.keys["U"]:
            self.no_others()
            self.ui.frame.after(40, self.ui.snake.up)
            # snake.up()
        if self.keys["D"]:
            self.no_others()
            self.ui.frame.after(40, self.ui.snake.down)
            # snake.down()
        if self.keys["L"]:
            self.no_others()
            self.ui.frame.after(40, self.ui.snake.left)
            # snake.left()
        if self.keys["R"]:
            self.no_others()
            self.ui.frame.after(40, self.ui.snake.right)
            # snake.right()

        self.ui.frame.after(16, self.move_snake)




