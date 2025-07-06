import numpy as np
import random
from pac_man.pac_gym import FlattenObsWrapper, obs_to_state
from pac_man.pac_gym import PacManEnv
from pac_man.ppo import PPO
from pac_man.logger import logger

def test_random_agent(n_episodes=20):
    env = PacManEnv()

    for ep in range(n_episodes):
        obs = env.reset()
        total_reward = 0
        step_count = 0
        done = False

        print(f"\n=== Episode {ep+1} ===")
        while not done:
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            total_reward += reward
            step_count += 1

            env.render()

        print(f"Episode finished in {step_count} steps. Total reward: {total_reward}")

    env.close()



def test_agent():
    
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
    done = False
    agent = PPO(state_dim, action_dim, config)
    agent.load(checkpoint_path="Models\\ToMPacMan")
    logger.info(f"Model loaded")
    total_reward = 0

    while not done:
        action, *_ = agent.select_action(dummy_state)
        dummy_state, reward, done, info, _ = wrapped_env.step(action)
        total_reward+=reward
        wrapped_env.render()
    wrapped_env.close()
    logger.info(f"total reward : {total_reward}")

if __name__ == "__main__":
    test_agent()

