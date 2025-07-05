import pygame

# Maze Layout
MAZE_LAYOUT = [
    "1111111111111111111111111111111111111",
    "1000000000100000000100000000000000001",
    "1001100000000011000001100000000011101",
    "1000000000100000000100101111101001001",
    "1111011110111101111100101000001001001",
    "1000010000100001000000001001001000001",
    "1111010111101111011101111100011011111",
    "1000000100000100000100000001001000001",
    "1011111110101111110101011100001111101",
    "1000000000100000000001000001000000001",
    "1111111111111111111111111111111111111"
]

TILE_SIZE = 40
ROWS = len(MAZE_LAYOUT)
COLS = len(MAZE_LAYOUT[0])

SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE

BLUE = (0, 0, 255)
DOT_COLOR = (255, 200, 100)
FRUIT_COLOR = (255, 0, 0)

# Initialize coins: True if path, False if wall
coins = [
    [cell == '0' for cell in row]
    for row in MAZE_LAYOUT
]

# For demo: place a "fruit" in the center
fruit_position = (ROWS // 2, COLS // 2)

def draw_maze(screen):
    # Draw walls and coins
    for row_idx, row in enumerate(MAZE_LAYOUT):
        for col_idx, tile in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if tile == '1':
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
            elif coins[row_idx][col_idx]:
                # Draw coin/dot
                pygame.draw.circle(
                    screen,
                    DOT_COLOR,
                    (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
                    TILE_SIZE // 8
                )
    # Draw the fruit
    fx, fy = fruit_position
    pygame.draw.circle(
        screen,
        FRUIT_COLOR,
        (fy * TILE_SIZE + TILE_SIZE // 2, fx * TILE_SIZE + TILE_SIZE // 2),
        TILE_SIZE // 4
    )

def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Custom Pac-Man")
    return screen

def init_coins():
    return [
        [cell == '0' for cell in row]
        for row in MAZE_LAYOUT
    ]

def is_coin_at(row, col, coins):
    return coins[row][col]

def remove_coin(row, col, coins):
    coins[row][col] = False

def draw_maze(screen, coins):
    for row_idx, row in enumerate(MAZE_LAYOUT):
        for col_idx, tile in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if tile == '1':
                pygame.draw.rect(screen, (0, 0, 255), (x, y, TILE_SIZE, TILE_SIZE))
            elif coins[row_idx][col_idx]:
                pygame.draw.circle(screen, (255, 200, 100), (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 8)



def get_wall_rects():
    wall_rects = []
    for row_idx, row in enumerate(MAZE_LAYOUT):
        for col_idx, tile in enumerate(row):
            if tile == '1':
                rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                wall_rects.append(rect)
    return wall_rects