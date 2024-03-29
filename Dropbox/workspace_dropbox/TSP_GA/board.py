import pygame
from constants import BLACK, BACKGROUND_PANEL

class Board:
    def __init__(self, x: float, y: float, width: float, height: float, margin: float = 5):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__margin = margin
        self.points = []

    def get_margin(self):
        return self.__margin

    def get_position(self) -> tuple:
        return (self.__x, self.__y)
        
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height
    
    def get_margin(self):
        return self.__margin


    def render(self, screen):
        pygame.draw.rect(screen, BLACK, (self.__x, self.__y, self.__width, self.__height))
        pygame.draw.rect(screen, BACKGROUND_PANEL, (self.__x + self.__margin, self.__y + self.__margin, self.__width - 2*self.__margin, self.__height - 2*self.__margin))



    # kiểm tra con trỏ chuột có đang ở trong bảng hay không
    def is_mouse_over(self, mouse_x, mouse_y):
        return ((self.__x + self.__margin) < mouse_x < (self.__x + self.__width - self.__margin) and 
               (self.__y + self.__margin) < mouse_y < (self.__y + self.__height - self.__margin))