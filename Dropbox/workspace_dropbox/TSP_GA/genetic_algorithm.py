from point import Point
from individual import Individual
from population import Population

class GeneticAlgorithm:
    def __init__(self, cities, population_size, mutation_rate, mutate_func_id):
        self.__population = self.__create_population(cities, population_size)
        self.__mutate_func_id = mutate_func_id
        self.__population.set_mutate_rate(mutation_rate)
        self.__mutation_rate = mutation_rate

    def get_population_size(self):
        return self.__population.get_size()
    
    def get_individual_size(self):
        return self.__population[0].get_size()
    
    def get_mutate_rate(self):
        return self.__population.get_mutate_rate()
    
    def set_mutate_rate(self, rate):
        self.__population.set_mutate_rate(rate)

    def resize_population(self, new_size : int):
        self.__population.resize(new_size)

    def run(self):
        if (self.__population.get_size() < 2):
            return

        new_population = self.__population.generate_new_population(self.__mutate_func_id)
        self.__population.natural_selection(new_population)

    def extend(self, points: list[tuple[int, int]]):
        self.__population.extend([Point(i) for i in points])

    def __create_population(self, points: list[tuple[int, int]], population_size: int):
        individual = Individual([Point(i) for i in points])
        population = Population(individual, population_size)
        return population

    def get_best_individual(self):
        return self.__population.get_best_individual()

    def get_best_sum_distance(self):
        return self.__population[0].get_sum_distance()
