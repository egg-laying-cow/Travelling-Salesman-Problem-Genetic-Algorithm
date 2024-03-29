import random
from individual import Individual
from point import Point

class Population:
    def __init__(self, individual : "Individual", population_size : int, mutation_rate = 30):
        self.size = population_size
        self.__list = self.init_population(individual)
        self.__mutation_rate = mutation_rate

    def __getitem__(self, index: int) -> Individual:
        return self.__list[index]
    
    def get_mutate_rate(self):
        return self.__mutation_rate
    
    def set_mutate_rate(self, rate):
        self.__mutation_rate = rate

    def resize(self, new_size : int):
        if new_size < self.size:
            self.__list = self.__list[:new_size]
        elif new_size > self.size:
            while len(self.__list) < new_size:
                points = self.__list[0][:-1]
                random.shuffle(points)
                points.append(self.__list[0][-1])
                self.__list.append(Individual(points))
            self.__list.sort(key = lambda x: x.get_sum_distance())
        self.size = new_size

    def extend(self, points: list["Point"]):
        for i in range(len(self.__list)):
            self.__list[i].extend(points)
        self.__list.sort(key = lambda x: x.get_sum_distance())

    def init_population(self, individual : "Individual") -> list:
        population = [individual]
        for i in range(self.size - 1):
            points = individual[:-1]
            random.shuffle(points)
            points.append(individual[-1])
            population.append(Individual(points))
        population.sort(key = lambda x: x.get_sum_distance())
        return population
    
    def mutate(self, child : list):
        if len(child) < 3:
            return
        c = random.randint(0, 100)
        if c < self.__mutation_rate:
            self.inversion_mutation(child)

    def swap_mutation(self, child : list):
        i, j = random.sample(range(0, len(child) - 1), 2)
        child[i], child[j] = child[j], child[i]

    def insert_mutation(self, child : list):
        i, j = random.sample(range(0, len(child) - 1), 2)
        child.insert(i, child.pop(j))

    def scramble_mutation(self, child : list):
        i, j = random.sample(range(0, len(child) - 1), 2)
        if i > j:
            i, j = j, i
        temp = child[i:j+1]
        random.shuffle(temp)
        child[i:j+1] = temp

    def inversion_mutation(self, child : list): ####
        i, j = random.sample(range(0, len(child) - 1), 2)
        if i > j:
            i, j = j, i
        child[i:j+1] = child[i:j+1][::-1]

    def displacement_mutation(self, child : list):
        i, j = random.sample(range(0, len(child) - 1), 2)
        if i > j:
            i, j = j, i
        temp = child[i:j+1]
        temp_child = child[:i] + child[j+1:]
        k = random.randint(0, len(temp_child) - 1)
        child.clear()
        child.extend(temp_child[:k] + temp + temp_child[k:])
        
    def crossover(self, parent1 : "Individual", parent2 : "Individual") -> "Individual":
        p = random.randint(1, parent1.get_size() - 1)
        child = parent1[:p]
        for point in parent2:
            if point not in child:
                child.append(point)

        self.mutate(child)
        return Individual(child)
    
    def generate_new_population(self) -> list:
        population = self.__list[:(self.size // 2)]
        population1 = self.__list[:((self.size * 3) // 4)]

        new_population = []
        for i in range(self.size):
            parent1 = random.choice(population)
            parent2 = random.choice(population1)
            child1 = self.crossover(parent1, parent2)
            new_population.append(child1)
            child2 = self.crossover(parent2, parent1)
            new_population.append(child2)
        new_population.sort(key = lambda x: x.get_sum_distance())
        return new_population
    
    def natural_selection(self, new_population : list):
        """Chọn lọc tự nhiên"""
        population = []

        # chọn lọc tự nhiên, để số lượng cá thể không thay đổi
        i, j = 0, 0
        while (len(population) < self.size):
            if (i >= self.size):
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
        
if (__name__ == "__main__"):
    # test 
    print("test ham displacement_mutation")
    child = [Point(1, 2), Point(3,4), Point(5, 6), Point(7, 8), Point(9, 10), Point(11, 12), Point(13, 14), Point(15, 16), Point(17, 18), Point(19, 20)]
    print("child ban đầu:", child)
    population = Population(Individual([Point(1, 2), Point(3,4), Point(5, 6), Point(7, 8), Point(9, 10), Point(11, 12), Point(13, 14), Point(15, 16), Point(17, 18), Point(19, 20)]), 10)
    population.inversion_mutation(child)
    for i in range(len(child)):
        print(child[i].get_position())