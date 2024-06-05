import math

class Point(tuple):   
    def __new__(cls, position: tuple):
        return super().__new__(cls, position)
    
    def get_distance_to(self, other: "Point") -> float:
        return math.sqrt((self[0] - other[0])**2 + (self[1] - other[1])**2)



