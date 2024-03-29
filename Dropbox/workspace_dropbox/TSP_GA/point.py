import pygame
from constants import BLACK, WHITE, RED

class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_position(self):
        return (self.__x, self.__y)
    
    def render(self, screen):
        pygame.draw.circle(screen, RED, (self.__x, self.__y), 4)
        pygame.draw.circle(screen, WHITE, (self.__x, self.__y), 2)

    def get_distance_to(self, other):
        return ((self.__x - other.get_position()[0])**2 + (self.__y - other.get_position()[1])**2)**0.5

    