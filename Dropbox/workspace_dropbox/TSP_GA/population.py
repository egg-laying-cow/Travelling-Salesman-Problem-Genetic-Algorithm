import random
from individual import Individual
from point import Point

class Population:
    def __init__(self, individual : "Individual", population_size : int, mutation_rate = 30):
        self.__list = self.__init_population(individual, population_size)
        self.__mutation_rate = mutation_rate

    def __getitem__(self, index: int) -> Individual:
        return self.__list[index]
    
    def get_mutate_rate(self):
        return self.__mutation_rate
    
    def set_mutate_rate(self, rate):
        self.__mutation_rate = rate

    def get_size(self):
        return len(self.__list)

    def resize(self, new_size : int):
        if new_size < len(self.__list):
            self.__list = self.__list[:new_size]
        elif new_size > len(self.__list):
            while len(self.__list) < new_size:
                points = self.__list[0][:-1]
                random.shuffle(points)
                points.append(self.__list[0][-1])
                self.__list.append(Individual(points))
            self.__list.sort(key = lambda x: x.get_sum_distance())

    def extend(self, points: list["Point"]):
        for i in range(len(self.__list)):
            self.__list[i].extend(points)
        self.__list.sort(key = lambda x: x.get_sum_distance())

    def __init_population(self, individual : "Individual", population_size) -> list:
        population = [individual]
        for i in range(population_size - 1):
            points = individual[:-1]
            random.shuffle(points)
            points.append(individual[-1])
            population.append(Individual(points))
        population.sort(key = lambda x: x.get_sum_distance())
        return population
    
    def get_best_individual(self) -> Individual:
        return self.__list[0].get_list()
        
    def crossover(self, parent1: "Individual", parent2: "Individual", mutate_func_id: int) -> "Individual":
        p = random.randint(1, parent1.get_size() - 1)
        child = parent1[:p]
        for point in parent2:
            if point not in child:
                child.append(point)

        child = Individual(child)
        child.mutate(self.__mutation_rate, mutate_func_id)
        return child
    
    def generate_new_population(self, mutate_func_id) -> list:
        population = self.__list[:(len(self.__list) // 2)]
        population1 = self.__list[:((len(self.__list) * 3) // 4)]

        new_population = []
        for i in range(len(self.__list)):
            parent1 = random.choice(population)
            parent2 = random.choice(population1)
            child1 = self.crossover(parent1, parent2, mutate_func_id)
            new_population.append(child1)
            child2 = self.crossover(parent2, parent1, mutate_func_id)
            new_population.append(child2)
        new_population.sort(key = lambda x: x.get_sum_distance())
        return new_population
    
    def natural_selection(self, new_population : list):
        """Chọn lọc tự nhiên"""
        population = []

        # chọn lọc tự nhiên, để số lượng cá thể không thay đổi
        i, j = 0, 0
        while (len(population) < len(self.__list)):
            if i >= len(self.__list):
                population.append(new_population[j])
                j += 1
            elif (j >= len(new_population)):
                population.append(self.__list[i])
                i += 1
            elif (self.__list[i].get_sum_distance() < new_population[j].get_sum_distance()):
                population.append(self.__list[i])
                i += 1
            else:
                population.append(new_population[j])
                j += 1
        self.__list = population
    
    def check_stop_condition(self) -> bool:
        """Kiểm tra điều kiện dừng"""
        pass
        
