import pygame
import random
from button import Button
from board import Board
from genetic_algorithm import GeneticAlgorithm
from helper import BACKGROUND, BLACK, render_text, render_connected_lines, render_mouse_position, render_points

class TSP:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.mouse_x, self.mouse_y = 0, 0

        self.genetic_algorithm_running = False
        self.iteration = 0
        self.points = []
        self.point_set = set()
        self.mutation_rate = 30
        self.sum_distance = 0
        self.ga = None
        
        self.population_size = 100

        self.font_path = pygame.font.match_font('sans')
        self.font = pygame.font.Font(self.font_path, 20)
        self.font_small = pygame.font.Font(self.font_path, 15)

        self.board = Board(50, 50, 700, 500)
        self.population_size_button_plus = Button(self.board.get_position()[0] + self.board.get_width() + 100,
                                                 self.board.get_position()[1] + self.board.get_height() - 500, 55, 45)
        self.population_size_button_minus = Button(self.board.get_position()[0] + self.board.get_width() + 195,
                                                 self.board.get_position()[1] + self.board.get_height() - 500, 55, 45)
        self.mutation_rate_button_plus = Button(self.board.get_position()[0] + self.board.get_width() + 100,
                                               self.board.get_position()[1] + self.board.get_height() - 409, 55, 45)
        self.mutation_rate_button_minus = Button(self.board.get_position()[0] + self.board.get_width() + 195,
                                                self.board.get_position()[1] + self.board.get_height() - 409, 55, 45)
        self.random_button = Button(self.board.get_position()[0] + self.board.get_width() + 100,
                                   self.board.get_position()[1] + self.board.get_height() - 318, 150, 45)
        self.run_button = Button(self.board.get_position()[0] + self.board.get_width() + 100, 
                                self.board.get_position()[1] + self.board.get_height() - 227, 150, 45)
        self.stop_button = Button(self.board.get_position()[0] + self.board.get_width() + 100,
                                self.board.get_position()[1] + self.board.get_height() - 136, 150, 45)
        self.reset_button = Button(self.board.get_position()[0] + self.board.get_width() + 100, 
                                self.board.get_position()[1] + self.board.get_height() - 45, 150, 45)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60) 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.board.is_mouse_over(self.mouse_x, self.mouse_y):
                    self.add_point(self.mouse_x, self.mouse_y)
                elif self.run_button.is_mouse_over(self.mouse_x, self.mouse_y):
                    if (len(self.points) >= 3):
                        self.genetic_algorithm_running = True
                elif self.reset_button.is_mouse_over(self.mouse_x, self.mouse_y):
                    self.reset()
                elif self.stop_button.is_mouse_over(self.mouse_x, self.mouse_y):
                    self.genetic_algorithm_running = False    
                elif self.random_button.is_mouse_over(self.mouse_x, self.mouse_y):
                    self.reset_for_random()
                    self.get_random_points()
                elif self.mutation_rate_button_plus.is_mouse_over(self.mouse_x, self.mouse_y):
                    if self.mutation_rate <= 99:
                        self.mutation_rate += 1
                elif self.mutation_rate_button_minus.is_mouse_over(self.mouse_x, self.mouse_y):
                    if self.mutation_rate >= 1:
                        self.mutation_rate -= 1
                elif self.population_size_button_plus.is_mouse_over(self.mouse_x, self.mouse_y):
                    if self.population_size < 2000:
                        self.population_size += 10
                elif self.population_size_button_minus.is_mouse_over(self.mouse_x, self.mouse_y):
                    if self.population_size > 10:
                        self.population_size -= 10

    def update(self):
        self.update_mouse_position()
        if self.genetic_algorithm_running:
            self.run_genetic_algorithm()
        
    def render(self):
        pygame.display.flip()
        self.screen.fill(BACKGROUND)
        self.board.render(self.screen)
        render_mouse_position(self.board, self.screen, self.mouse_x, self.mouse_y, self.font_small)
        render_text(self.screen, f"Points: {len(self.points)}", self.board.get_position()[0],
                    self.board.get_position()[1] + self.board.get_height() + 10, self.font)
        render_text(self.screen, f"Iteration: {self.iteration}", self.board.get_position()[0] + 100, 
                    self.board.get_position()[1] + self.board.get_height() + 10, self.font)
        render_text(self.screen, f"Population size: {self.population_size}",
                    self.population_size_button_minus.get_position()[0] + self.population_size_button_minus.get_width() + 10,
                    self.population_size_button_minus.get_position()[1] + self.population_size_button_minus.get_height() // 2, self.font)
        render_text(self.screen, f"Mutation rate: {self.mutation_rate}",
                    self.mutation_rate_button_minus.get_position()[0] + self.mutation_rate_button_minus.get_width() + 10,
                    self.mutation_rate_button_minus.get_position()[1] + self.mutation_rate_button_minus.get_height() // 2, self.font)
        render_text(self.screen, f"Sum distance: {self.sum_distance:.2f}",
                    self.board.get_position()[0] + self.board.get_width() - 175, 
                    self.board.get_position()[1] + self.board.get_height() + 10, self.font)
        
        self.run_button.render(self.screen, "Run", self.font)
        self.reset_button.render(self.screen, "Reset", self.font)
        self.stop_button.render(self.screen, "Stop", self.font)
        self.random_button.render(self.screen, "Random", self.font)
        self.mutation_rate_button_plus.render(self.screen, "+", self.font)
        self.mutation_rate_button_minus.render(self.screen, "-", self.font)
        self.population_size_button_plus.render(self.screen, "+", self.font)
        self.population_size_button_minus.render(self.screen, "-", self.font)

        if self.iteration > 0:
            render_connected_lines(self.points, self.screen)
        render_points(self.points, self.screen)

    def update_mouse_position(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def add_point(self, x, y):
        if (x, y) not in self.point_set:
            self.points.append((x, y))
            self.point_set.add((x, y))

    def get_random_points(self):
        self.points = []
        self.point_set = set()
        n = random.randint(30, 150)
        for i in range(n):
            x = random.randint(self.board.get_position()[0] + self.board.get_margin(), 
                               self.board.get_position()[0] + self.board.get_width() - self.board.get_margin())
            y = random.randint(self.board.get_position()[1] + self.board.get_margin(), 
                               self.board.get_position()[1] + self.board.get_height() - self.board.get_margin())
            self.add_point(x, y)
    
    # hàm sử dụng thuật toán di truyền để tìm đường đi ngắn nhất
    def run_genetic_algorithm(self):
        if (len(self.points) < 2):
            return
        
        if self.ga is None:
            self.ga = GeneticAlgorithm(self.points, self.population_size, self.mutation_rate, 0)
        if (self.ga.get_individual_size() < len(self.points)):    
            self.ga.extend(self.points[self.ga.get_individual_size():])
        if (self.ga.get_population_size() != self.population_size):
            self.ga.resize_population(self.population_size)
            
        self.ga.set_mutate_rate(self.mutation_rate)
        self.ga.run()
        self.points = self.ga.get_best_individual()
        self.sum_distance = self.ga.get_best_sum_distance()
    
        self.iteration += 1

    def reset_for_random(self):
        self.ga = None
        self.iteration = 0
        self.sum_distance = 0
        self.genetic_algorithm_running = False

    def reset(self):
        self.reset_for_random()
        self.points = []
        self.point_set = set()
        self.population_size = 100
        self.mutation_rate = 30

if __name__ == "__main__":
    tsp = TSP()
    tsp.run()