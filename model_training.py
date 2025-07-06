from pac_man.pac_gym import PacManEnv
from pac_man.ppo import PPO, Trainer
import time

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

if __name__ == "__main__":
    

    env = PacManEnv()

    wrapped_env = FlattenObsWrapper(env)
    dummy_state, _ = wrapped_env.reset()
    state_dim = len(dummy_state)
    action_dim = env.action_space.n

    state_dim = len(obs_to_state(env.reset()))
    action_dim = env.action_space.n

    config = {
        'gamma': 0.99,
        'eps_clip': 0.2,
        'K_epochs': 4,
        'lr_actor': 1e-4,
        'lr_critic': 1e-3,
        'max_training_timesteps': int(3e6),  # Adjust as needed
        'max_ep_len': 1000,                  # Max timesteps per episode
        'update_timestep': 1000 * 4,            # How often to update PPO
        'log_freq': 1000 * 2,                   # How often to log
        'print_freq': 2000 * 5,                 # How often to print stats
        'save_model_freq': int(1e5)           # How often to save model
    }


    agent = PPO(state_dim, action_dim, config)
    # agent.load("your_checkpoint_folder")   # <- if you have a trained model
    trainer = Trainer(agent, wrapped_env, config)

    trainer.train()


