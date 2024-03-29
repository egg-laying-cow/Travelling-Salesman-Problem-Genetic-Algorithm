import pygame

BACKGROUND_PANEL = (252,246,232)
BACKGROUND = (219,207,195)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

def render_text(screen, text, x, y, font):
    text = font.render(text, True, BLACK)
    screen.blit(text, (x, y))

def render_connected_lines(points, screen):
    if (len(points) < 2):
        return
    
    for i in range(len(points) - 1):
        pygame.draw.line(screen, BLACK, points[i].get_position(), points[i + 1].get_position(), 3)
    if (len(points) > 2):
        pygame.draw.line(screen, BLACK, points[len(points) - 1].get_position(), points[0].get_position(), 3)

def render_mouse_position(board, screen, mouse_x, mouse_y, font):
    if board.is_mouse_over(mouse_x, mouse_y):
        text_mouse = font.render("(" + str(mouse_x - board.get_position()[0] - board.get_margin()) + "," + 
                                            str(mouse_y - board.get_position()[1] - board.get_margin()) + ")",True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))