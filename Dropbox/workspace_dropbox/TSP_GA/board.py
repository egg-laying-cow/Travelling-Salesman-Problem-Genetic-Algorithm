import pygame
from helper import BLACK, BACKGROUND_PANEL

class Board:
    def __init__(self, x: float, y: float, width: float, height: float, margin: float = 5):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._margin = margin
        self.points = []

    def get_margin(self):
        return self._margin

    def get_position(self) -> tuple:
        return (self._x, self._y)
        
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def get_margin(self):
        return self._margin

    def render(self, screen):
        pygame.draw.rect(screen, BLACK, (self._x, self._y, self._width, self._height))
        pygame.draw.rect(screen, BACKGROUND_PANEL, (self._x + self._margin, self._y + self._margin, self._width - 2*self._margin, self._height - 2*self._margin))

    # kiểm tra con trỏ chuột có đang ở trong bảng hay không
    def is_mouse_over(self, mouse_x, mouse_y):
        return ((self._x + self._margin) < mouse_x < (self._x + self._width - self._margin) and 
               (self._y + self._margin) < mouse_y < (self._y + self._height - self._margin))