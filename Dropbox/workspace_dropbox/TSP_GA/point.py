import pygame
from helper import BLACK, WHITE, RED

class Point:
    def __init__(self, position: tuple):
        self.__position = position

    def get_position(self) -> tuple:
        return self.__position
    
    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, RED, (self.__position[0], self.__position[1]), 4)
        pygame.draw.circle(screen, WHITE, (self.__position[0], self.__position[1]), 2)

    def get_distance_to(self, other: "Point") -> float:
        return ((self.__position[0] - other.get_position()[0])**2 + (self.__position[1] - other.get_position()[1])**2)**0.5

    