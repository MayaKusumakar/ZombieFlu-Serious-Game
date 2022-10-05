from gym.envs.registration import register

register(
    id='ZGame-v0',
    entry_point='gym_zgame.envs.ZGameEnv:ZGame'
)
