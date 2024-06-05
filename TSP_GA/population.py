import random
from individual import Individual
from point import Point

class Population:
    def __init__(self, individual : "Individual", population_size : int, mutation_rate = 30):
        self.__list = self.__init_population(individual, population_size)

    def __getitem__(self, index: int) -> Individual:
        return self.__list[index]

    def get_size(self):
        return len(self.__list)

    def resize(self, new_size : int):
        if new_size < len(self.__list):
            self.__list = self.__list[:new_size]
        elif new_size > len(self.__list):
            while len(self.__list) < new_size:
                new_individual = self.__list[0].create_new_individual()
                self.__list.append(new_individual)
            self.__list.sort(key = lambda x: x.get_sum_distance())

    def extend(self, points: list["Point"]):
        for i in range(len(self.__list)):
            self.__list[i].extend(points)
        self.__list.sort(key = lambda x: x.get_sum_distance())

    def __init_population(self, individual : "Individual", population_size) -> list:
        population = [individual]
        for i in range(population_size - 1):
            new_individual = individual.create_new_individual()
            population.append(new_individual)
        population.sort(key = lambda x: x.get_sum_distance())
        return population
    
    def get_best_individual(self) -> Individual:
        return self.__list[0].get_list()
    
    def crossover(self, parent1: "Individual", parent2: "Individual", mutation_rate, mutate_func_id: int) -> "Individual":
        p = random.randint(1, parent1.get_size() - 1)
        child = parent1[:p]

        child_set = set(child)
        child.extend([point for point in parent2 if point not in child_set])

        child = Individual(child)
        child.mutate(mutation_rate, mutate_func_id)
        return child
    
    def generate_new_population(self, mutation_rate, mutate_func_id) -> list:
        population1 = self.__list[:(len(self.__list) // 2)]
        population2 = self.__list

        new_population = []
        for _ in range(len(self.__list)):
            parent1 = random.choice(population1)
            parent2 = random.choice(population2)
            new_population.append(self.crossover(parent1, parent2, mutation_rate, mutate_func_id))
            new_population.append(self.crossover(parent2, parent1, mutation_rate, mutate_func_id))
        new_population.sort(key = lambda x: x.get_sum_distance())
        return new_population
    
    def natural_selection(self, new_population : list):
        """Chọn lọc tự nhiên"""
        population1 = self.__list
        population2 = new_population

        population1_length = len(population1)
        population2_length = len(population2)

        merged_population = []

        # chọn lọc tự nhiên, để số lượng cá thể không thay đổi
        i, j = 0, 0
        while (len(merged_population) < population1_length):
            if i >= population1_length:
                merged_population.append(population2[j])
                j += 1
            elif j >= population2_length:
                merged_population.append(population1[i])
                i += 1
            elif population1[i].get_sum_distance() < population2[j].get_sum_distance():
                merged_population.append(population1[i])
                i += 1
            else:
                merged_population.append(population2[j])
                j += 1
                
        self.__list = merged_population
    
    def check_stop_condition(self) -> bool:
        """Kiểm tra điều kiện dừng"""
        pass
        
