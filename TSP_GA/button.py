from board import Board
from helper import BLACK

class Button(Board):
    def __init__(self, x: float, y: float, width: float, height: float, text: str = "", margin: float = 5):
        super().__init__(x, y, width, height, margin)
        self.__text = text

    def render(self, screen, text, font):
        super().render(screen)
        text_button = font.render(text, True, BLACK)
        screen.blit(text_button, (self._x + self._width // 2 - text_button.get_width() // 2, 
                                  self._y + self._height // 2 - text_button.get_height() // 2))
