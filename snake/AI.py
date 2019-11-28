import os
import numpy
import random
from snake.main import SnakeAPP


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
                with open(os.path.join(os.getcwd(), "snake/data/genetic_data"), 'w') as file:
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
                with open(os.path.join(os.getcwd(), "snake/data/generation"), 'w') as file:
                    file.write(str(self.generation))
            except FileNotFoundError:
                pass

        # Save food coordinates:
        if fittest.food_position != '':
            try:
                with open(os.path.join(os.getcwd(), 'snake/data/food_coord'), 'w') as file:
                    file.write(str(fittest.food_position))
            except FileNotFoundError:
                pass

        # Save fittest fitness and generation number:
        if Population.plot_data != '':
            try:
                with open(os.path.join(os.getcwd(), 'snake/data/plot_graph'), 'a') as file:
                    to_write = Population.plot_data
                    file.write(str(to_write))
            except FileNotFoundError:
                print('file not found')
