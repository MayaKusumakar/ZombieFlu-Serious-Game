import gym
from gym import spaces
import math
import json
from gym_zgame.envs.enums import PLAY_TYPE
from gym_zgame.envs.model.City import City
from gym_zgame.envs.enums.PLAYER_ACTIONS import DEPLOYMENTS, LOCATIONS
from gym_zgame.envs.Print_Colors.PColor import PBack, PFore, PFont
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import multiprocessing
import random
from multiprocessing import Queue


class ZGame(gym.Env):

    def __init__(self, demo=True, human_log_name = 'human_log.json', machine_log_name = 'machine_log.json',
                 rl_log_name='train_info.json',
                 config_name='play_config.json'):
        # Tunable parameters

        self.play_type = PLAY_TYPE.MACHINE  # Defaults only, set in main classes
        self.render_mode = 'machine'
        self.RL_LOG_FILENAME = rl_log_name
        self.HUMAN_LOG_NAME = human_log_name
        self.MACHINE_LOG_NAME = machine_log_name
        self.CONFIG_FILENAME = config_name

        self.config = {}
        with open(self.CONFIG_FILENAME) as file:
            data = json.load(file)
            self.config.update(data)

        self.mode = self.config["mode"]
        self.demo = bool(self.config["demo"])
        self.who_play = self.config["who"]  # machine or human

        # CONSTANTS
        self.MAX_TURNS = self.config["max_turns"]
        self.collect_interval = 0

        # Main parameters
        self.city = City()
        self.total_score = 0
        self.turn = 0
        self.done = False
        # Defining spaces
        self._num_locations = len(LOCATIONS)
        self._num_deployments = len(DEPLOYMENTS)
        self._num_actions = self._num_locations * self._num_deployments
        self.action_space = spaces.MultiDiscrete([2*self._num_actions, 2*self._num_actions])
        self.observation_space = spaces.Box(low=0, high=200, shape=(10, 6 + (self.MAX_TURNS * 2)), dtype='uint8')

        self.reset()
        self.end_stats = {}
        self.reward = []

        self.collection_counter = 0

        # keeps track of step number for graphing purposes
        self.step_counter = 0
        self.x_counter = []

        self.store = []

        # self.y_values = []
        self.alive = []
        self.dead = []
        self.ashen = []
        self.human = []
        self.zombie = []
        self.healthy = []
        self.flu = []
        self.immune = []

        self.score_hist = []

        if self.demo == True:
            self.q_npc = Queue()
            multiprocessing.Process(target=self.plot_npc_graph, args=(self.q_npc,)).start()

            self.q_score = Queue()
            multiprocessing.Process(target=self.plot_score_graph, args=(self.q_score,)).start()

        print('initialize finish')

    def get_gen_info(self):
        # contains: {
        # total score, reward, list of actions,
        # alive, dead, ashen, human, zombie, healthy, flu}
        info = {}
        info = {
            'score': self.city.score,
            'reward': self.reward,
            'total_score': self.total_score
        }
        if self.mode == "play":
            info.update({'deployments': self.city.turn_deployments})
        else:
            info.update({'deployments': self.city.all_deployments}) # want to know what actions it took at any given state
        return info

    def get_city_info(self):
        info = {
            'alive': self.city.num_alive,
            'dead': self.city.num_dead,
            'ashen': self.city.num_ashen,
            'human': self.city.num_human,
            'zombie': self.city.num_zombie,
            'healthy': self.city.num_healthy,
            'flu': self.city.num_flu,
            'immune': self.city.num_immune
        }
        return info

    def collect_stats(self):
        self.end_stats.update(self.get_gen_info())
        self.end_stats.update(self.get_city_info())
        self.end_stats.update({'reward': self.reward})
        self.end_stats.update({'total_score': self.total_score})

    def write_to_log(self, filename):
        with open(filename, 'a') as f_:
            f_.write(json.dumps(self.end_stats) + '\n')
        self.end_stats = {}

    # plots npc stats
    def plot_npc_graph(self, q_npc):
        print("entered plot_npc_graph()")
        fig, axs = plt.subplots(3, sharex=True, sharey=True)
        fig.suptitle('NPC Trends')

        def animate(i):
            alive, dead, ashen, human, zombie, healthy, flu, immune = q_npc.get()
            # plt.cla()
            # plt.plot(alive, dead, ashen)
            axs[0].plot(alive, color='blue')
            axs[0].plot(dead, color='orange')
            axs[0].plot(ashen, color='green')
            axs[1].plot(human, color='blue')
            axs[1].plot(zombie, color='orange')
            axs[2].plot(healthy, color='blue')
            axs[2].plot(flu, color='orange')
            axs[2].plot(immune, color='green')

            axs[0].legend(['Alive', 'Dead', 'Ashen'])
            axs[1].legend(['Human', 'Zombie'])
            axs[2].legend(['Healthy', 'Flu', 'Immune'])


        plt.xlabel('Every game')
        plt.ylabel('Number of NPC type')

        ani = FuncAnimation(plt.gcf(), animate)
        plt.tight_layout()
        plt.show()
        print("exiting plot_graph() process")

    def process_npc_graph_data(self):
        # for i in range(self.collect_interval):
        self.x_counter.append(self.step_counter)
        self.alive.append(self.city.num_alive)
        self.dead.append(self.city.num_dead)
        self.ashen.append(self.city.num_ashen)
        self.human.append(self.city.num_human)
        self.zombie.append(self.city.num_zombie)
        self.healthy.append(self.city.num_healthy)
        self.flu.append(self.city.num_flu)
        self.immune.append(self.city.num_immune)

        # if len(self.alive) > 200:
        #     self.alive.pop(0)
        #     self.dead.pop(0)
        #     self.ashen.pop(0)
        # time.sleep(1)
        self.q_npc.put([self.alive, self.dead, self.ashen,
                    self.human, self.zombie,
                    self.healthy, self.flu, self.immune])

    # plots score changes
    def plot_score_graph(self, q_score):
        print("entered plot_deployment_graph()")

        plt.suptitle('Score')

        def animate(i):

            score = q_score.get()
            plt.plot(score)

        plt.xlabel('Every 14 steps')
        plt.ylabel('Score')

        ani = FuncAnimation(plt.gcf(), animate)
        plt.tight_layout()
        plt.show()
        print("exiting plot_graph() process")

    def process_score_graph_data(self):
        # for i in range(self.collect_interval):
        # if len(self.alive) > 200:
        #     self.alive.pop(0)
        #     self.dead.pop(0)
        #     self.ashen.pop(0)
        # time.sleep(1)

        # x values set during initialization >>> x_deployments
        self.score_hist.append(self.city.total_score)
        self.q_score.put(self.score_hist)



    def reset(self):
        self.city = City()
        self.total_score = 0
        self.turn = 0
        self.done = False
        self._num_locations = len(LOCATIONS)
        self._num_deployments = len(DEPLOYMENTS)
        self._num_actions = self._num_locations * self._num_deployments
        self.action_space = spaces.MultiDiscrete([2*self._num_actions, 2*self._num_actions])
        self.observation_space = spaces.Box(low=0, high=200, shape=(10, 6 + (self.MAX_TURNS * 2)), dtype='uint8')
        obs = self.get_obs()
        return obs

    def step(self, actions):
        self.collection_counter += 1
        self.step_counter += 1
        # Convert actions
        formatted_actions = self.decode_raw_action(actions=actions)
        # Adjudicate turn
        score, done = self._do_turn(formatted_actions)
        # Update score and turn counters
        self.total_score += score
        self.turn += 1
        # Check if done
        if done or (self.turn >= self.MAX_TURNS):
            self.done = True
        # Report out basic information for step
        obs = self.get_obs()
        info = {'turn': self.turn, 'step_reward': score, 'total_reward': self.total_score}
        self.reward = score
        self.collect_stats()

        if self.mode == "train":
            self.collect_interval = self.config["train_collection_interval"]
        else:  # for human/machine play, not training
            self.collect_interval = self.config["play_collection_interval"]

        if self.collection_counter == self.collect_interval:
            if self.mode == "train":
                self.write_to_log(self.RL_LOG_FILENAME)
            else:
                if self.who_play == "human":
                    self.write_to_log(self.HUMAN_LOG_NAME)
                else:
                    self.write_to_log(self.MACHINE_LOG_NAME)
            self.collection_counter = 0
            if self.demo == True:
                self.process_npc_graph_data()
                self.process_score_graph_data()



        return obs, self.total_score, self.done, info

    def _do_turn(self, actions):
        score, done = self.city.do_turn(actions=actions)
        return score, done

    def get_obs(self):
        if self.play_type == PLAY_TYPE.HUMAN:
            return self.city.human_encode()
        elif self.play_type == PLAY_TYPE.MACHINE:
            return self.city.rl_encode()
        else:
            raise ValueError('Failed to find acceptable play type.')

    def render(self, mode='human'):
        if self.render_mode == 'human' or mode == 'human':
            return self.city.human_render()
        elif self.render_mode == 'machine' or mode == 'machine':
            return self.city.rl_render()
        else:
            raise ValueError('Failed to find acceptable play type.')

    @staticmethod
    def encode_raw_action(add_1, location_1, deployment_1, add_2 = None, location_2=None, deployment_2=None):
        # Takes in locations and deployments and converts it to a pair of ints that matches the action space def
        # Think of it as a 2d array where rows are locations and columns are deployments
        # Then, the 2d array is unwrapped into a 1d array where the 2nd row starts right after the first
        # 0 to LOCATIONS * DEPLOYMENTS-1 is adding a deployment, and LOCATIONS*DEPLOYMENTS to 2*LOCATIONS*DEPLOYMENTS-1 is removing
        action_1 = add_1 * len(LOCATIONS) * len(DEPLOYMENTS) + location_1.value * len(DEPLOYMENTS) + deployment_1.value
        action_2 = add_2 * len(LOCATIONS) * len(DEPLOYMENTS) + location_2.value * len(DEPLOYMENTS) + deployment_2.value
        return [action_1, action_2]

    @staticmethod
    def decode_raw_action(actions):
        # Reverse process of the encoding, takes in a list of raw actions and returns a list of model ready actions
        # Modular arithmetic to the rescue
        readable_actions = []
        for action in actions:
            if action >= len(LOCATIONS) * len(DEPLOYMENTS):
                add_int = 1
                action -= len(LOCATIONS) * len(DEPLOYMENTS)
            else:
                add_int = 0
            location_int = action // len(DEPLOYMENTS)  # gets the quotient
            deployment_int = action % len(DEPLOYMENTS)  # gets the remainder
            readable_actions.append([add_int, LOCATIONS(location_int), DEPLOYMENTS(deployment_int)])
        return readable_actions

    @staticmethod
    def print_player_action_selections():
        # Build up console output
        fbuffer = '********************************************************************************************'
        ebuffer = '********************************************************************************************'
        player_action_string = PBack.green + fbuffer + PBack.reset + '\n'
        player_action_string += PBack.green + '**||' + PBack.reset + \
                                PBack.orange + ' LOCATIONS'.ljust(13) + PBack.reset + \
                                PBack.green + '||' + PBack.reset + \
                                PBack.orange + ' DEPLOYEMENTS'.ljust(69) + PBack.reset + \
                                PBack.green + '||**' + PBack.reset + '\n'

        num_locations = len(LOCATIONS)
        num_deployments = len(DEPLOYMENTS)
        num_rows = math.ceil(num_deployments / 2)
        col_width = 13
        for i in range(num_rows):
            loc_val = LOCATIONS(i).value if i < num_locations else '--'
            loc_name = LOCATIONS(i).name if i < num_locations else '--'
            dep1_val = DEPLOYMENTS(i).value if i < num_deployments else '--'
            dep1_name = DEPLOYMENTS(i).name if i < num_deployments else '--'
            dep2_val = DEPLOYMENTS(i + num_rows).value if (i + num_rows) < num_deployments else '--'
            dep2_name = DEPLOYMENTS(i + num_rows).name if (i + num_rows) < num_deployments else '--'
            pair_1 = ' {0} - {1}'.format(loc_val, loc_name)
            pair_2 = ' {0} - {1}'.format(dep1_val, dep1_name)
            pair_3 = ' {0} - {1}'.format(dep2_val, dep2_name)
            player_action_string += PBack.green + '**||' + PBack.reset + \
                                    pair_1.ljust(col_width) + \
                                    PBack.green + '||' + PBack.reset + \
                                    pair_2.ljust(col_width + 18) + \
                                    PBack.green + '||' + PBack.reset + \
                                    pair_3.ljust(col_width + 23) + \
                                    PBack.green + '||**' + PBack.reset + '\n'

        player_action_string += PBack.green + ebuffer + PBack.reset
        print(player_action_string)
        return player_action_string
