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

