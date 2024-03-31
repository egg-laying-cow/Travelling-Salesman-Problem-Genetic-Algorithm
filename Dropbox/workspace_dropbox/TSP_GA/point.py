import pygame
from helper import BLACK, WHITE, RED

class Point(tuple):   
    def __new__(cls, x, y):
        return super().__new__(cls, (x, y))
    
    def get_distance_to(self, other: "Point") -> float:
        return ((self[0] - other[0])**2 + (self[1] - other[1])**2)**0.5

