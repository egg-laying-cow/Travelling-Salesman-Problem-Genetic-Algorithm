from random import randint, shuffle
from point import Point

class Individual:
    def __init__(self, points: list[Point]):
        self.__list = points
        self.__sum_distance = self.__get_sum_distance()
        self.__mutate_functions = (
            self.__inversion_mutate,
            self.__displacement_mutate,
            self.__scramble_mutate,
            self.__insert_mutate,
            self.__swap_mutate
        )

    def create_new_individual(self):
        points = self.__list[:-1]
        shuffle(points)
        points.append(self.__list[-1])
        return Individual(points)

    def __getitem__(self, index: int):
        return self.__list[index]

    def __get_sum_distance(self) -> float:
        sum_distance = 0
        if len(self.__list) > 1:
            for i in range(len(self.__list) - 1):
                sum_distance += self.__list[i].get_distance_to(self.__list[i + 1])
            if (len(self.__list) > 2):
                sum_distance += self.__list[-1].get_distance_to(self.__list[0])
        return sum_distance    
    
    def get_sum_distance(self) -> float:
        return self.__sum_distance
    
    def get_list(self) -> list:
        return self.__list.copy()
    
    def get_size(self) -> int:
        return len(self.__list)
    
    def extend(self, points: list[Point]) -> None:
        self.__list.extend(points)
        self.__sum_distance = self.__get_sum_distance()

    def get_mutate_function_name(self, mutate_func_id: int) -> str:
        mutate_func_name = self.__mutate_functions[mutate_func_id].__name__
        mutate_func_name = mutate_func_name[2:]
        mutate_func_name = mutate_func_name.replace("_", " ")
        mutate_func_name = mutate_func_name.replace("mutate", "mutation")
        return mutate_func_name

    def mutate(self, mutation_rate: int, mutate_func_id: int) -> None:
        if len(self.__list) < 3:
            return

        if randint(0, 100) < mutation_rate:
            self.__mutate_functions[mutate_func_id % len(self.__mutate_functions)]()
            self.__sum_distance = self.__get_sum_distance()

    def __displacement_mutate(self):
        length_list = len(self.__list)
        i = randint(0, length_list - 3)
        j = randint(i + 1, length_list - 2)

        temp = self.__list[i:j+1]
        self.__list = self.__list[:i] + self.__list[j+1:]
        k = randint(0, len(self.__list) - 1)
        self.__list = self.__list[:k] + temp + self.__list[k:]

    def __inversion_mutate(self): ####
        length_list = len(self.__list)
        i = randint(0, length_list - 3)
        j = randint(i + 1, length_list - 2)
        self.__list[i:j+1] = self.__list[i:j+1][::-1]
    
    def __scramble_mutate(self):
        length_list = len(self.__list)
        i = randint(0, length_list - 3)
        j = randint(i + 1, length_list - 2)

        temp = self.__list[i:j+1]
        shuffle(temp)
        self.__list[i:j+1] = temp

    def __insert_mutate(self):
        length_list = len(self.__list)
        i = randint(0, length_list - 3)
        j = randint(i + 1, length_list - 2)
        self.__list.insert(i, self.__list.pop(j))
    
    def __swap_mutate(self):
        length_list = len(self.__list)
        i = randint(0, length_list - 3)
        j = randint(i + 1, length_list - 2)
        self.__list[i], self.__list[j] = self.__list[j], self.__list[i]

    
    
