import pygame
from screen import initialize_screen, draw_maze, MAZE_LAYOUT, TILE_SIZE, init_coins, is_coin_at, remove_coin
from agent import PacMan
from ghost import Ghost, blinky_target, pinky_target, inky_target, clyde_target

def get_wall_rects():
    wall_rects = []
    for row_idx, row in enumerate(MAZE_LAYOUT):
        for col_idx, tile in enumerate(row):
            if tile == '1':
                rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                wall_rects.append(rect)
    return wall_rects

def main():
    screen = initialize_screen()
    clock = pygame.time.Clock()
    wall_rects = get_wall_rects()
    coins = init_coins()

    # Pac-Man start
    pacman = PacMan(x=1 * TILE_SIZE, y=1 * TILE_SIZE, walls=wall_rects)

    # Ghosts: positions and scatter targets (row, col)
    blinky = Ghost(x=13 * TILE_SIZE, y=1 * TILE_SIZE, walls=wall_rects, get_target_func=blinky_target, scatter_target=(0, len(MAZE_LAYOUT[0]) - 1))
    pinky  = Ghost(x=15 * TILE_SIZE, y=1 * TILE_SIZE, walls=wall_rects, get_target_func=pinky_target, scatter_target=(0, 0))
    inky   = Ghost(x=13 * TILE_SIZE, y=3 * TILE_SIZE, walls=wall_rects, get_target_func=inky_target, scatter_target=(len(MAZE_LAYOUT) - 1, len(MAZE_LAYOUT[0]) - 1))
    clyde  = Ghost(x=15 * TILE_SIZE, y=3 * TILE_SIZE, walls=wall_rects, get_target_func=clyde_target, scatter_target=(len(MAZE_LAYOUT) - 1, 0))

    ghosts = [blinky, pinky, inky, clyde]
    ghost_colors = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]  # Red, Pink, Cyan, Orange

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze(screen, coins)

        keys = pygame.key.get_pressed()
        pacman.handle_input(keys)
        pacman.move()
        pacman.draw(screen)

        # Collect coins
        if pacman.rect.x % TILE_SIZE == 0 and pacman.rect.y % TILE_SIZE == 0:
            row = pacman.rect.y // TILE_SIZE
            col = pacman.rect.x // TILE_SIZE
            if is_coin_at(row, col, coins):
                remove_coin(row, col, coins)

        # Move and draw ghosts
        for ghost, color in zip(ghosts, ghost_colors):
            # Inky uses blinky reference for targeting
            if ghost is inky:
                ghost.move(pacman, blinky)
            else:
                ghost.move(pacman)
            ghost.draw(screen, color)

        # Simple collision with ghosts (game over)
        for ghost in ghosts:
            if pacman.rect.colliderect(ghost.rect):
                print("GAME OVER")
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
