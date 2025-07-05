import numpy as np
import random

from pac_man.pac_gym import PacManEnv

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

if __name__ == "__main__":
    test_random_agent()

