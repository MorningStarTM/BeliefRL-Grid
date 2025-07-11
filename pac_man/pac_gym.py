import gym
import numpy as np

from pac_man.screen import MAZE_LAYOUT, TILE_SIZE, init_coins, get_wall_rects, draw_maze, SCREEN_HEIGHT, SCREEN_WIDTH, ROWS, COLS
from pac_man.agent import PacMan, DIRS
from pac_man.ghost import Ghost, blinky_target, pinky_target, inky_target, clyde_target
import pygame
from gym.spaces import Dict, Discrete, MultiBinary, Box



class PacManEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super().__init__()
        # Action space: 0=LEFT, 1=RIGHT, 2=UP, 3=DOWN, 4=NOOP
        self.action_space = gym.spaces.Discrete(5)
        
        self.last_pacman_action = 4  # 4=NOOP
        self.last_ghost_actions = [4, 4, 4, 4]  # Assume 4=NOOP for all at start

        # Observation space: build a feature vector for positions, maze, coins, directions
        rows = len(MAZE_LAYOUT)
        cols = len(MAZE_LAYOUT[0])
        # For simplicity: flat (row, col) for all agents, flattened coins (0/1 per cell), + directions
        n_features = 2 + 1 + 1 + 2*4 + 4 + 4 + (rows * cols)

        self.observation_space = Dict({
                    "pacman": Dict({
                        "pos": Box(0, max(ROWS, COLS), shape=(2,), dtype=np.int32),
                        "direction": Box(-1, 1, shape=(2,), dtype=np.int32),
                        "last_action": Discrete(5)
                    }),
                    "ghosts": Box(
                        low=np.array([[-1, -1, 0, 0, 0]]*4),    # shape (4, 5) -- no last_action
                        high=np.array([[ROWS, COLS, 1, 1, 1]]*4),
                        shape=(4, 5),
                        dtype=np.int32
                    ),
                    "coins": MultiBinary(ROWS * COLS)
                })


        
        self.walls = get_wall_rects()
        self.reset()

    def reset(self):
        self.coins = init_coins()
        self.pacman = PacMan(x=1 * TILE_SIZE, y=1 * TILE_SIZE, walls=self.walls)
        self.blinky = Ghost(x=13 * TILE_SIZE, y=1 * TILE_SIZE, walls=self.walls, get_target_func=blinky_target, scatter_target=(0, len(MAZE_LAYOUT[0]) - 1))
        self.pinky  = Ghost(x=15 * TILE_SIZE, y=1 * TILE_SIZE, walls=self.walls, get_target_func=pinky_target, scatter_target=(0, 0))
        self.inky   = Ghost(x=13 * TILE_SIZE, y=3 * TILE_SIZE, walls=self.walls, get_target_func=inky_target, scatter_target=(len(MAZE_LAYOUT) - 1, len(MAZE_LAYOUT[0]) - 1))
        self.clyde  = Ghost(x=15 * TILE_SIZE, y=3 * TILE_SIZE, walls=self.walls, get_target_func=clyde_target, scatter_target=(len(MAZE_LAYOUT) - 1, 0))
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        self.score = 0
        self.done = False
        return self._get_obs()

    def step(self, action):
        if self.done:
            return self._get_obs(), 0, True, {}
        
        self.last_pacman_action = action

        # 1. Pac-Man: set direction from action
        if action < 4:
            # Map action to DIRS used by your PacMan class, or set self.pacman.next_direction
            self.pacman.next_direction = list(DIRS.values())[action]
        self.pacman.move()
        
        # 2. Collect coin if at center
        reward = 0
        if self.pacman.rect.x % TILE_SIZE == 0 and self.pacman.rect.y % TILE_SIZE == 0:
            row = self.pacman.rect.y // TILE_SIZE
            col = self.pacman.rect.x // TILE_SIZE
            if self.coins[row][col]:
                self.coins[row][col] = False
                reward += 1
                self.score += 1

        for idx, ghost in enumerate(self.ghosts):
            prev_pos = (ghost.rect.x, ghost.rect.y)
            if ghost is self.inky:
                ghost.move(self.pacman, self.blinky)
            else:
                ghost.move(self.pacman)
            dx = ghost.rect.x - prev_pos[0]
            dy = ghost.rect.y - prev_pos[1]
            dir_idx = 4  # NOOP default
            if dx < 0 and dy == 0:
                dir_idx = 0  # LEFT
            elif dx > 0 and dy == 0:
                dir_idx = 1  # RIGHT
            elif dx == 0 and dy < 0:
                dir_idx = 2  # UP
            elif dx == 0 and dy > 0:
                dir_idx = 3  # DOWN
            self.last_ghost_actions[idx] = dir_idx


        
        # 4. Check collision
        for ghost in self.ghosts:
            if self.pacman.rect.colliderect(ghost.rect):
                reward -= 10
                self.done = True
                break

        # 5. Check win
        if all(not coin for row in self.coins for coin in row):
            reward += 10
            self.done = True

        return self._get_obs(), reward, self.done, {}

    def _get_obs(self):
        VISION_RADIUS = 3  # or your chosen distance
        pac_row = self.pacman.rect.y // TILE_SIZE
        pac_col = self.pacman.rect.x // TILE_SIZE
        pac_dir = [int(np.sign(self.pacman.direction.x)), int(np.sign(self.pacman.direction.y))]
        pac_last = self.last_pacman_action

        ghosts_array = np.full((4, 5), -1, dtype=np.int32)  # Masked by default: [-1, -1, 0, 0, 0]
        for i, ghost in enumerate(self.ghosts):
            row = ghost.rect.y // TILE_SIZE
            col = ghost.rect.x // TILE_SIZE
            dist = abs(row - pac_row) + abs(col - pac_col)
            if dist <= VISION_RADIUS:
                dir_x = int(np.sign(ghost.direction.x))
                dir_y = int(np.sign(ghost.direction.y))
                state = int(ghost.state == 'CHASE')
                ghosts_array[i] = [row, col, dir_x, dir_y, state]
            # else, remains masked as [-1, -1, 0, 0, 0]

        flat_coins = np.array([int(cell) for row in self.coins for cell in row], dtype=np.int8)

        obs = {
            "pacman": {
                "pos": np.array([pac_row, pac_col], dtype=np.int32),
                "direction": np.array(pac_dir, dtype=np.int32),
                "last_action": pac_last
            },
            "ghosts": ghosts_array,
            "coins": flat_coins
        }
        return obs



    def render(self, mode='human'):
        if not hasattr(self, 'screen'):
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Pac-Man Gym Env")
        self.screen.fill((0, 0, 0))

        draw_maze(self.screen, self.coins)
        self.pacman.draw(self.screen)
        ghost_colors = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
        for ghost, color in zip(self.ghosts, ghost_colors):
            ghost.draw(self.screen, color)

        pygame.display.flip()
        pygame.event.pump()  # Allows window to stay responsive

    def close(self):
        if hasattr(self, 'screen'):
            pygame.quit()



class FlattenObsWrapper:
    """Wrap PacManEnv to flatten obs to 1D state (numpy array) for PPO agent."""
    def __init__(self, env):
        self.env = env

    def reset(self):
        obs = self.env.reset()
        return obs_to_state(obs), {}

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        return obs_to_state(obs), reward, done, False, info

    def render(self, *args, **kwargs):
        self.env.render(*args, **kwargs)

    def close(self):
        self.env.close()




def obs_to_state(obs):
        # Example: flatten all obs into 1D numpy array (adjust if your model expects differently)
        state = []
        state.extend(obs['pacman']['pos'].tolist())
        state.extend(obs['pacman']['direction'].tolist())
        state.append(obs['pacman']['last_action'])
        state.extend(obs['ghosts'].flatten().tolist())
        state.extend(obs['coins'].tolist())
        return state