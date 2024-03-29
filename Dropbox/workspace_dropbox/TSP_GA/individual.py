from point import Point

class Individual:
    def __init__(self, points: list[Point]):
        self.__list = points
        self.__sum_distance = self.__get_sum_distance()
    
    def __getitem__(self, index: int):
        return self.__list[index]

    def __get_sum_distance(self) -> float:
        sum_distance = 0
        if len(self.__list) > 1:
            for i in range(len(self.__list) - 1):
                sum_distance += self.__list[i].get_distance_to(self.__list[i + 1])
            if (len(self.__list) > 2):
                sum_distance += self.__list[len(self.__list) - 1].get_distance_to(self.__list[0])
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
    
