import pygame
import random
import time

TILE_SIZE = 40
MOVE_SPEED = 4

DIRS = [
    pygame.Vector2(-MOVE_SPEED, 0),
    pygame.Vector2(MOVE_SPEED, 0),
    pygame.Vector2(0, -MOVE_SPEED),
    pygame.Vector2(0, MOVE_SPEED),
]

class Ghost:
    def __init__(self, x, y, walls, get_target_func, scatter_target):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.walls = walls
        self.direction = random.choice(DIRS)
        self.state = 'SCATTER'
        self.get_target_func = get_target_func
        self.scatter_target = scatter_target
        self.state_timer = time.time()
        self.state_interval = 7  # start with 7 seconds SCATTER

    def can_move(self, direction):
        next_rect = self.rect.move(direction)
        return not any(next_rect.colliderect(wall) for wall in self.walls)

    def switch_state(self):
        now = time.time()
        if self.state == 'SCATTER' and now - self.state_timer > 7:
            self.state = 'CHASE'
            self.state_timer = now
        elif self.state == 'CHASE' and now - self.state_timer > 20:
            self.state = 'SCATTER'
            self.state_timer = now

    def get_tile_pos(self):
        return (self.rect.y // TILE_SIZE, self.rect.x // TILE_SIZE)

    def move(self, pacman, blinky=None):
        self.switch_state()
        if self.rect.x % TILE_SIZE == 0 and self.rect.y % TILE_SIZE == 0:
            # Find all available directions (not reversing)
            reverse_dir = -self.direction
            possible_dirs = [d for d in DIRS if self.can_move(d) and d != reverse_dir]
            if not possible_dirs:
                possible_dirs = [d for d in DIRS if self.can_move(d)]
            # Determine target
            if self.state == 'SCATTER':
                target = self.scatter_target
            else:
                target = self.get_target_func(self, pacman, blinky)
            # Pick direction minimizing Manhattan distance to target
            my_pos = self.get_tile_pos()
            def dist(dir):
                next_pos = (my_pos[0] + int(dir.y // MOVE_SPEED), my_pos[1] + int(dir.x // MOVE_SPEED))
                return abs(next_pos[0] - target[0]) + abs(next_pos[1] - target[1])
            self.direction = min(possible_dirs, key=dist)
        # Move in current direction
        if self.can_move(self.direction):
            self.rect = self.rect.move(self.direction)

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, self.rect.center, TILE_SIZE // 2 - 4)

# ---- Ghost Personalities ----

def blinky_target(self, pacman, blinky):
    # Directly chase Pac-Man's current tile
    return (pacman.rect.y // TILE_SIZE, pacman.rect.x // TILE_SIZE)

def pinky_target(self, pacman, blinky):
    # Four tiles ahead of Pac-Man's direction
    dir_vec = pacman.direction
    ahead_row = (pacman.rect.y + dir_vec.y * 4) // TILE_SIZE
    ahead_col = (pacman.rect.x + dir_vec.x * 4) // TILE_SIZE
    return (int(ahead_row), int(ahead_col))

def inky_target(self, pacman, blinky):
    # Uses Blinky and a point two tiles ahead of Pac-Man
    dir_vec = pacman.direction
    two_ahead_row = (pacman.rect.y + dir_vec.y * 2) // TILE_SIZE
    two_ahead_col = (pacman.rect.x + dir_vec.x * 2) // TILE_SIZE
    # Vector from Blinky through this point, doubled
    if blinky:
        v_row = two_ahead_row - (blinky.rect.y // TILE_SIZE)
        v_col = two_ahead_col - (blinky.rect.x // TILE_SIZE)
        return (int((blinky.rect.y // TILE_SIZE) + 2 * v_row), int((blinky.rect.x // TILE_SIZE) + 2 * v_col))
    else:
        return (int(two_ahead_row), int(two_ahead_col))

def clyde_target(self, pacman, blinky):
    # If far from Pac-Man, chase him. If close, scatter to home.
    ghost_row, ghost_col = self.get_tile_pos()
    pac_row, pac_col = (pacman.rect.y // TILE_SIZE, pacman.rect.x // TILE_SIZE)
    distance = abs(ghost_row - pac_row) + abs(ghost_col - pac_col)
    if distance > 8:
        return (pac_row, pac_col)
    else:
        return self.scatter_target

