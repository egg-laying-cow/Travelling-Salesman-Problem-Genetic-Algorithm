from point import Point

class Individual:
    def __init__(self, points: list[Point]):
        self.size = len(points)
        self.__list = points
        self.sum_distance = self.get_sum_distance()
    
    def __getitem__(self, index: int) -> Point:
        return self.__list[index]

    def get_sum_distance(self) -> float:
        sum_distance = 0
        if len(self.__list) > 1:
            for i in range(self.size - 1):
                sum_distance += self.__list[i].get_distance_to(self.__list[i + 1])
            if (self.size > 2):
                sum_distance += self.__list[self.size - 1].get_distance_to(self.__list[0])

        return sum_distance
    
    def get_list(self):
        return self.__list.copy()
    
    def extend(self, points: list[Point]):
        self.__list.extend(points)
        self.size = len(self.__list)
        self.sum_distance = self.get_sum_distance()
    
