import uuid
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAY_TYPE import PLAY_TYPE
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import A2C
import json


class ZGame:
    """
    RL Algorithm: A2C
    Original paper: https://arxiv.org/abs/1602.01783
    OpenAI blog post: https://openai.com/blog/baselines-acktr-a2c/
    https://stable-baselines.readthedocs.io/en/master/modules/a2c.html
    """
    def __init__(self, model_filename='rl-agent', training_config='play_config.json', analysis_log_file='train_info.json'):
        self.ENV_NAME = 'ZGame-v0'
        self.MODEL_FILENAME = model_filename
        self.CONFIG_FILENAME = training_config
        self.ANALYSIS_FILENAME = analysis_log_file
        self.GAME_ID = uuid.uuid4()
        self.env = None
        self.current_actions = []
        self.config = {}

        with open(self.CONFIG_FILENAME) as file:
            data = json.load(file)
            self.config.update(data)

        self.turn = 0
        self.max_turns = self.config["max_turns"]
        # Learning Parameters
        self._verbosity = 1
        self.num_steps = self.config["num_steps"]
        self.num_envs = self.config["num_envs"]
        self.collect_interval = self.config["train_collection_interval"]
        # Always do these actions upon start
        self._setup()

    def _setup(self):
        # Game parameters
        self.env = make_vec_env(self.ENV_NAME, n_envs=self.num_envs)
        self.env.play_type = PLAY_TYPE.MACHINE
        self.env.render_mode = 'machine'
        self.env.MAX_TURNS = self.max_turns
        self.env.reset()
        # Report success
        print('Created new environment {0} with GameID: {1}'.format(self.ENV_NAME, self.GAME_ID))

    def done(self):
        print("Episode finished after {} turns".format(self.turn))
        self._cleanup()

    def _cleanup(self):
        self.env.close()

    def run(self):
        print('Starting new game for training!')
        model = A2C(MlpPolicy, self.env, verbose=self._verbosity)
        model.learn(total_timesteps=self.num_steps)
        model.save(self.MODEL_FILENAME)
