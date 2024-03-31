from individual import Individual
from point import Point
from individual import Individual
from population import Population

class GeneticAlgorithm:
    def __init__(self, cities, population_size, mutation_rate, mutate_func_id):
        self.__population = self.__create_population(cities, population_size)
        self.__mutate_func_id = mutate_func_id
        self.__population.set_mutate_rate(mutation_rate)
        self.__mutation_rate = mutation_rate

    def get_size(self):
        return self.__population.get_size()
    
    def get_individual_size(self):
        return self.__population[0].get_size()
    
    def get_mutate_rate(self):
        return self.__population.get_mutate_rate()
    
    def set_mutate_rate(self, rate):
        self.__population.set_mutate_rate(rate)

    def resize(self, new_size : int):
        self.__population.resize(new_size)

    def run(self):
        if (self.__population.get_size() < 2):
            return

        new_population = self.__population.generate_new_population(self.__mutate_func_id)
        self.__population.natural_selection(new_population)

    def extend(self, cities: list[tuple[int, int]]):
        points = [Point(city[0], city[1]) for city in cities]
        self.__population.extend(points)

    def get_best_individual(self):
        return self.__population.get_best_individual()

    def __create_population(self, cities: list[tuple[int, int]], population_size):
        individual = Individual([Point(city[0], city[1]) for city in cities])
        population = Population(individual, population_size)
        return population

    def get_best_sum_distance(self):
        return self.__population[0].get_sum_distance()
