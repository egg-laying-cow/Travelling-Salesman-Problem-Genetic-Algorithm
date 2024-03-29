import pygame
import random
from board import Board
from point import Point
from individual import Individual
from population import Population
from constants import BACKGROUND, BLACK, WHITE

class TSP:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.screen = pygame.display.set_mode((1200, 700))
        self.mouse_x, self.mouse_y = 0, 0
        self.board = Board(50, 50, 700, 500)

        self.population_size_button_plus = Board(self.board.get_position()[0] + self.board.get_width() + 100,
                                                 self.board.get_position()[1] + self.board.get_height() - 500, 55, 45)
        self.population_size_button_minus = Board(self.board.get_position()[0] + self.board.get_width() + 195,
                                                 self.board.get_position()[1] + self.board.get_height() - 500, 55, 45)
        self.mutation_rate_button_plus = Board(self.board.get_position()[0] + self.board.get_width() + 100,
                                               self.board.get_position()[1] + self.board.get_height() - 409, 55, 45)
        self.mutation_rate_button_minus = Board(self.board.get_position()[0] + self.board.get_width() + 195,
                                                self.board.get_position()[1] + self.board.get_height() - 409, 55, 45)
        self.random_button = Board(self.board.get_position()[0] + self.board.get_width() + 100,
                                   self.board.get_position()[1] + self.board.get_height() - 318, 150, 45)
        self.run_button = Board(self.board.get_position()[0] + self.board.get_width() + 100, 
                                self.board.get_position()[1] + self.board.get_height() - 227, 150, 45)
        self.stop_button = Board(self.board.get_position()[0] + self.board.get_width() + 100,
                                self.board.get_position()[1] + self.board.get_height() - 136, 150, 45)
        self.reset_button = Board(self.board.get_position()[0] + self.board.get_width() + 100, 
                                self.board.get_position()[1] + self.board.get_height() - 45, 150, 45)

        self.font_path = pygame.font.match_font('sans')
        self.font = pygame.font.Font(self.font_path, 20)
        self.font_small = pygame.font.Font(self.font_path, 15)

        self.iteration = 0
        self.iteration_max = 10000
        self.points = []
        self.point_set = set()
        self.mutation_rate = 30
        self.sum_distance = 0

        self.population = None
        self.population_size = 100
        self.genetic_algorithm_running = False


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
                    self.population = None
                    self.iteration = 0
                    self.sum_distance = 0
                    self.genetic_algorithm_running = False
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
        if self.genetic_algorithm_running and self.iteration < self.iteration_max:
            self.run_genetic_algorithm()
        
    def render(self):
        pygame.display.flip()
        self.screen.fill(BACKGROUND)
        self.board.render(self.screen)
        self.render_mouse_position()
        self.render_points()

        self.render_points_count()
        self.render_iteration()
        self.render_population_size()
        self.render_mutation_rate()
        self.render_sum_distance()
        
        self.render_button(self.run_button, "Run")
        self.render_button(self.reset_button, "Reset")
        self.render_button(self.stop_button, "Stop")
        self.render_button(self.random_button, "Random")
        self.render_button(self.mutation_rate_button_plus, "+")
        self.render_button(self.mutation_rate_button_minus, "-")
        self.render_button(self.population_size_button_plus, "+")
        self.render_button(self.population_size_button_minus, "-")

        if self.iteration > 0:
            self.render_connected_lines()


    def update_mouse_position(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def render_mouse_position(self):
        if self.board.is_mouse_over(self.mouse_x, self.mouse_y):
            text_mouse = self.font_small.render("(" + str(self.mouse_x - self.board.get_position()[0]) + "," + str(self.mouse_y - self.board.get_position()[1]) + ")",True, BLACK)
            self.screen.blit(text_mouse, (self.mouse_x + 10, self.mouse_y))

    def render_points(self):
        for point in self.points:
            point.render(self.screen)

    def render_connected_lines(self):
        if (len(self.points) < 2):
            return
        
        for i in range(len(self.points) - 1):
            pygame.draw.line(self.screen, BLACK, self.points[i].get_position(), self.points[i + 1].get_position(), 3)
        if (len(self.points) > 2):
            pygame.draw.line(self.screen, BLACK, self.points[len(self.points) - 1].get_position(), self.points[0].get_position(), 3)    

    def render_points_count(self):
        text = self.font.render(f"Points: {len(self.points)}", True, BLACK)
        self.screen.blit(text, (self.board.get_position()[0], self.board.get_position()[1] + self.board.get_height() + 10))

    def render_iteration(self):
        text = self.font.render(f"Iteration: {self.iteration}", True, BLACK)
        self.screen.blit(text, (self.board.get_position()[0] + 100, self.board.get_position()[1] + self.board.get_height() + 10))

    def render_sum_distance(self):
        # text = self.font.render(f"Sum distance: {self.sum_distance}", True, BLACK)
        # chỉ lấy 2 chữ số sau dấu thập phân
        text = self.font.render(f"Sum distance: {self.sum_distance:.2f}", True, BLACK)
        self.screen.blit(text, (self.board.get_position()[0] + self.board.get_width() - 175, 
                                self.board.get_position()[1] + self.board.get_height() + 10))
    
    def render_button(self, button, text):
        button.render(self.screen)
        # vẽ chữ vào button
        text_button = self.font.render(text, True, BLACK)
        self.screen.blit(text_button, (button.get_position()[0] + button.get_width() // 2 - text_button.get_width() // 2, 
                                       button.get_position()[1] + button.get_height() // 2 - text_button.get_height() // 2))
        
    # Hàm in population size
    def render_population_size(self):
        text = self.font.render(f"Population size: {self.population_size}", True, BLACK)
        self.screen.blit(text, (self.population_size_button_minus.get_position()[0] + self.population_size_button_minus.get_width() + 10, 
                                self.population_size_button_minus.get_position()[1] + text.get_height() // 2))
        
    def render_mutation_rate(self):
        text = self.font.render(f"Mutation rate: {self.mutation_rate}", True, BLACK)
        self.screen.blit(text, (self.mutation_rate_button_minus.get_position()[0] + self.mutation_rate_button_minus.get_width() + 10, 
                                self.mutation_rate_button_minus.get_position()[1] + text.get_height() // 2))
        



    def add_point(self, x, y):
        if (x, y) not in self.point_set:
            self.points.append(Point(x, y))
            self.point_set.add((x, y))

    def get_random_points(self):
        self.points = []
        self.point_set = set()
        n = random.randint(30, 75)
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
        if self.population is None:
            self.population = Population(Individual(self.points), self.population_size)
        if (self.population[0].size != len(self.points)):
            self.population = Population(Individual(self.points), self.population_size)
        if (self.population.size != self.population_size):
            self.population.resize(self.population_size)
        
        self.population.set_mutate_rate(self.mutation_rate)
        new_population = self.population.generate_new_population()
        self.population.natural_selection(new_population)
        self.points = self.population[0].get_list()
        self.sum_distance = self.population[0].get_sum_distance()
        self.iteration += 1

    def reset(self):
        self.points = []
        self.point_set = set()
        self.population = None
        self.iteration = 0
        self.iteration_max = 10000
        self.population_size = 100
        self.mutation_rate = 30
        self.sum_distance = 0
        self.genetic_algorithm_running = False

if __name__ == "__main__":
    tsp = TSP()
    tsp.run()