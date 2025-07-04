# pac_man/agent.py
import pygame

YELLOW = (255, 255, 0)
TILE_SIZE = 40
MOVE_SPEED = 4

# Directions as vectors
DIRS = {
    "LEFT": pygame.Vector2(-MOVE_SPEED, 0),
    "RIGHT": pygame.Vector2(MOVE_SPEED, 0),
    "UP": pygame.Vector2(0, -MOVE_SPEED),
    "DOWN": pygame.Vector2(0, MOVE_SPEED),
    "NONE": pygame.Vector2(0, 0),
}

class PacMan:
    def __init__(self, x, y, walls):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.direction = DIRS["NONE"]
        self.next_direction = DIRS["NONE"]
        self.walls = walls

    def handle_input(self, keys):
        # Store next direction based on input
        if keys[pygame.K_LEFT]:
            self.next_direction = DIRS["LEFT"]
        elif keys[pygame.K_RIGHT]:
            self.next_direction = DIRS["RIGHT"]
        elif keys[pygame.K_UP]:
            self.next_direction = DIRS["UP"]
        elif keys[pygame.K_DOWN]:
            self.next_direction = DIRS["DOWN"]

    def on_grid(self):
        # Only allow direction change if Pac-Man is centered in the tile
        return (
            self.rect.x % TILE_SIZE == 0 and
            self.rect.y % TILE_SIZE == 0
        )

    def can_move(self, direction):
        next_rect = self.rect.move(direction)
        return not any(next_rect.colliderect(wall) for wall in self.walls)

    def move(self):
        # Only change direction at tile center
        if self.on_grid() and self.next_direction != DIRS["NONE"]:
            if self.can_move(self.next_direction):
                self.direction = self.next_direction
        # Try to move in current direction
        if self.can_move(self.direction):
            self.rect = self.rect.move(self.direction)
        else:
            self.direction = DIRS["NONE"]  # Stop if can't move

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.rect.center, TILE_SIZE // 2 - 4)
