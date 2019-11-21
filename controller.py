import re
from snake import model


class Controller:
    def __init__(self, load_population=False):
        self.ui = model.UI()
        self.neural_network = model.NeuralNetwork(snake=self.ui.snake)

        if load_population:
            self.population = model.Population(snake=self.ui.snake, load=self.load_genetic_data())
            self.population.generation = self.load_generation()
        else:
            self.population = model.Population(snake=self.ui.snake)

    def get_starting_screen(self):
        return self.ui.starting_screen

    def get_game_screen(self):
        return self.ui.game_screen

    def get_ai_screen(self):
        return self.ui.ai_screen

    def get_neural_network(self):
        return self.neural_network

    def load_fittest(self):
        return model.NeuralNetwork(snake=self.ui.snake, hidden_layer_data=self.load_genetic_data())

    @staticmethod
    def load_genetic_data():
        try:
            with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\genetic data.txt', 'r') as file:
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
            with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\generation.txt', 'r') as file:
                data = file.read()
                if data != '':
                    return int(data)
                else:
                    raise ValueError("Empty File")

        except FileNotFoundError:
            print("File Not Found")

    @staticmethod
    def load_food_coord():
        try:
            with open(r'C:\Users\Glaucio Nunes\PycharmProjects\Snake_AI\snake\food_coord.txt', 'r') as file:
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






