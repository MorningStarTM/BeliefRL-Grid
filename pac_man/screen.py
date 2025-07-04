import pygame

# Maze Layout (change as you want)
MAZE_LAYOUT = [
    "1111111111111111111111111111111111111",
    "1000000000100000000100000000000000001",
    "1001100000000011000001100000000011101",
    "1000000000100000000100101111101001001",
    "1111011110111101111100101000001001001",
    "0000010000100001000000001001001000001",
    "1111010111101111011101111100011011111",
    "1000000100000100000100000001001000001",
    "1011111110101111110101011100001111101",
    "1000000000100000000001000001000000001",
    "1111111111111111111111111111111111111"
]

TILE_SIZE = 40  # You can change this

ROWS = len(MAZE_LAYOUT)
COLS = len(MAZE_LAYOUT[0])

SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE

BLUE = (0, 0, 255)

def draw_maze(screen):
    for row_idx, row in enumerate(MAZE_LAYOUT):
        for col_idx, tile in enumerate(row):
            if tile == '1':
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Custom Pac-Man")
    return screen
