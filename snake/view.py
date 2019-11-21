import time
from tkinter import *
from snake import controller


class View:
    def __init__(self):
        self.bound = False
        self.ai_high_score = 0
        self.player_high_score = 0
        try:
            self.controller = controller.Controller(load_population=True)
        except ValueError:
            self.controller = controller.Controller()

        self.ui = self.controller.ui
        self.user_control = UserControl(self.ui)

    def ai_round(self, neural_network):
        neural_network.reset_lifespan()
        ai_screen = self.ui.ai_screen
        self.ui.snake.reset(self.ui.grid)
        self.ui.canvas.delete('all')

        while self.ui.snake.is_alive:
            # print(neural_network.lifespan)
            neural_network.food_position.append(self.ui.grid.food.get_coord())
            neural_network.decrease_lifespan()
            neural_network.increase_fitness()

            if self.ui.graphics:
                self.ui.draw_canvas()
                ai_screen.display_high_score(f'High Score: {self.ai_high_score}')
            self.ui.frame.update()
            decision = neural_network.make_decision()

            if decision == 'up':
                self.ui.snake.up()
            elif decision == 'down':
                self.ui.snake.down()
            elif decision == 'left':
                self.ui.snake.left()
            elif decision == 'right':
                self.ui.snake.right()

            time.sleep(self.ui.ai_tick)
            self.ui.snake.move()

            if self.ui.snake.is_apple_eaten:
                neural_network.increase_fitness(amount=neural_network.apple_increase)
                neural_network.reset_lifespan()
                self.ui.snake.is_apple_eaten = False

            self.ui.canvas.delete('all')

        self.ui.grid.generate_food()

        if self.ui.grid.score > self.ai_high_score:
            self.ai_high_score = self.ui.grid.score

        self.ui.grid.score = 0

    def goto_ai_screen(self):
        self.ui.top_frame.grid(row=0, column=0)
        self.unbind()
        self.ui.graphics = True
        self.ui.close_button_text.set('Menu')
        self.ui.current_screen = 'AI_SCREEN'
        population = self.controller.population

        try:
            while True:
                self.run_population(population=population)
                if self.ui.close:
                    population.save_genetic_data()
                    self.ui.close = False
                    break
                population.get_next_generation()

            for each in self.ui.top_frame.pack_slaves():
                each.pack_forget()
            self.goto_starting_screen()
        except TclError:
            print('TclError at (goto_ai_screen)')

    def run_population(self, population):
        for neural_network in population.members:
            self.ai_round(neural_network=neural_network)

        print(f'Fittest: {population.get_fittest().get_fitness()}, Average Fitness: {population.get_average_fitness()}')

    def goto_starting_screen(self, event=None):
        self.ui.canvas.delete("all")
        self.ui.top_frame.grid_forget()
        self.ui.plot_screen.plot_widget.grid_forget()

        self.ui.current_screen = 'STARTING_SCREEN'
        starting_screen = self.controller.get_starting_screen()
        starting_screen.create_buttons()

        self.ui.canvas.unbind("Button-1")
        self.ui.canvas.tag_bind(starting_screen.play_button, "<Button-1>", self.play_game)
        self.ui.canvas.tag_bind(starting_screen.ai_button, "<Button-1>", self.play_ai_mode)
        self.ui.canvas.tag_bind(starting_screen.fittest_display_button, "<Button-1>", self.goto_display_fittest)
        self.ui.canvas.tag_bind(starting_screen.plot_display_button, "<Button-1>", self.goto_plot_screen)

        self.ui.canvas.grid(row=1, column=0)

    def goto_plot_screen(self, event):
        self.ui.canvas.grid_forget()
        self.ui.top_frame.grid_forget()
        self.ui.plot_screen.show()
        self.ui.plot_screen.plot_widget.bind("<Button-1>", self.goto_starting_screen)

    def goto_game_screen(self):
        self.bind()
        self.ui.grid.score = 0
        self.ui.frame.after(0, self.user_control.move_snake)
        self.ui.snake.reset(self.ui.grid)
        self.ui.current_screen = 'GAME_SCREEN'

        self.ui.canvas.delete('all')
        try:
            # Player Game Loop:
            self.player_game_loop()

            self.ui.grid.generate_food()
            self.goto_starting_screen()
        except TclError:
            print('TclError')

    def display_fittest_performance(self):
        self.unbind()
        self.ui.grid.score = 0
        neural_network = self.controller.load_fittest()
        fittest_display_screen = self.ui.fittest_display_screen
        fittest_display_screen.close = False
        self.ui.canvas.bind("<Button-1>", fittest_display_screen.set_close)

        self.ui.current_screen = 'AI_SCREEN'
        self.ui.snake.reset(self.ui.grid)
        self.ui.canvas.delete('all')
        for each in self.controller.load_food_coord():
            if fittest_display_screen.close:
                self.goto_starting_screen()
                break
            neural_network.increase_fitness()
            self.ui.grid.food.set_coord(each)
            self.ui.fittest_display_screen.display_current_score(self.ui.grid.score)
            self.ui.draw_canvas()
            self.ui.fittest_display_screen.display_text(text=f'Fitness: {neural_network.fitness}')

            self.ui.frame.update()

            decision = neural_network.make_decision()
            if decision == 'up':
                self.ui.snake.up()
            elif decision == 'down':
                self.ui.snake.down()
            elif decision == 'left':
                self.ui.snake.left()
            elif decision == 'right':
                self.ui.snake.right()

            time.sleep(self.ui.watching_tick)
            self.ui.snake.move()

            if self.ui.snake.is_apple_eaten:
                neural_network.increase_fitness(amount=neural_network.apple_increase)
                neural_network.reset_lifespan()
                self.ui.snake.is_apple_eaten = False

            self.ui.canvas.delete('all')

        self.goto_starting_screen()

    def player_game_loop(self):
        while self.ui.snake.is_alive:
            self.ui.game_screen.display_current_score(current_score=self.ui.grid.score)
            self.ui.draw_canvas()
            self.ui.game_screen.display_high_score(high_score=f'High Score: {self.player_high_score}')
            self.ui.frame.update()
            self.ui.frame.after(self.ui.tick, self.ui.snake.move())
            self.ui.canvas.delete('all')

            if self.ui.grid.score > self.player_high_score:
                self.player_high_score = self.ui.grid.score

    def play_game(self, event):
        self.goto_game_screen()

    def play_ai_mode(self, event):
        self.goto_ai_screen()

    def goto_display_fittest(self, event):
        try:
            self.display_fittest_performance()
        except TclError:
            print('TclError')

    def bind(self):
        if not self.bound:
            self.bound = True
            frame = self.controller.ui.frame
            frame.bind("<KeyPress-Up>", self.user_control.up)
            frame.bind("<KeyPress-Down>", self.user_control.down)
            frame.bind("<KeyPress-Left>", self.user_control.left)
            frame.bind("<KeyPress-Right>", self.user_control.right)

    def unbind(self):
        if self.bound:
            self.bound = False
            frame = self.controller.ui.frame
            frame.unbind("<KeyPress-Up>")
            frame.unbind("<KeyPress-Down>")
            frame.unbind("<KeyPress-Left>")
            frame.unbind("<KeyPress-Right>")


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
