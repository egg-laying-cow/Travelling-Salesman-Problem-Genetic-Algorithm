import pygame
from helper import BLACK, WHITE, RED

class Point:
    def __init__(self, position: tuple):
        self.__position = position

    def get_position(self):
        return self.__position
    
    def render(self, screen):
        pygame.draw.circle(screen, RED, (self.__position[0], self.__position[1]), 4)
        pygame.draw.circle(screen, WHITE, (self.__position[0], self.__position[1]), 2)

    def get_distance_to(self, other):
        # return ((self.__x - other.get_position()[0])**2 + (self.__y - other.get_position()[1])**2)**0.5
        return ((self.__position[0] - other.get_position()[0])**2 + (self.__position[1] - other.get_position()[1])**2)**0.5

    