import pygame
from helper import BLACK, WHITE, RED

class Point:
    def __init__(self, position: tuple[int, int]):
        self.__position = position

    def get_position(self):
        return self.__position

    def get_distance_to(self, other: "Point") -> float:
        return ((self.__position[0] - other.get_position()[0])**2 + (self.__position[1] - other.get_position()[1])**2)**0.5

if __name__ == "__main__":
    a = Point((0, 0))
    b = Point((1, 1))
    print(a.get_distance_to(b)) # 1.4142135623730951
    z = []
    print(len(z))