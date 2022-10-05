import argparse
import gym
import gym_zgame
from gym_zgame.envs.enums.PLAYER_ACTIONS import LOCATIONS, DEPLOYMENTS

parser = argparse.ArgumentParser(description='CLI Argument Parser for Basic Testing.')
parser.add_argument('--action_encoding', help='Test encoding and decoding actions.', default=False, action='store_true')
parser.add_argument('--sample_actions', help='Print out sample actions.', type=int, default=0)
parser.add_argument('--state_structure', help='Print out state structure.', default=False, action='store_true')
parser.add_argument('--take_step', help='Take a random step and print results.', default=False, action='store_true')


def check_evn(action_encoding=False, sample_actions=0, state_structure=False, step=False):
    env = gym.make('ZGame-v0')
    if action_encoding:
        env.print_player_action_selections()
        test_action_1 = [0, 201]
        test_action_1_decoded = env.decode_raw_action(test_action_1)
        test_action_1_encoded = env.encode_raw_action(location_1=test_action_1_decoded[0][0],
                                                      deployment_1=test_action_1_decoded[0][1],
                                                      location_2=test_action_1_decoded[1][0],
                                                      deployment_2=test_action_1_decoded[1][1])
        print('Test 1:\nOriginal: {0}\nDecoded: {1}\nRecovered: {2}'.format(test_action_1,
                                                                            test_action_1_decoded,
                                                                            test_action_1_encoded))
        test_action_2 = [[LOCATIONS.CENTER, DEPLOYMENTS.FIREBOMB_BARRAGE],
                          [LOCATIONS.S, DEPLOYMENTS.BSL4LAB_SAFETY_ON]]
        test_action_2_encoded = env.encode_raw_action(location_1=test_action_2[0][0],
                                                      deployment_1=test_action_2[0][1],
                                                      location_2=test_action_2[1][0],
                                                      deployment_2=test_action_2[1][1])
        test_action_2_decoded = env.decode_raw_action(test_action_2_encoded)
        print('Test 2:\nOriginal: {0}\nDecoded: {1}\nRecovered: {2}'.format(test_action_2,
                                                                            test_action_2_encoded,
                                                                            test_action_2_decoded))

    for i in range(sample_actions):
        raw_actions = env.action_space.sample()
        readable_actions = env.decode_raw_action(raw_actions)
        print('Raw Action Sample {}: {}'.format(i, raw_actions))
        print('Readable Action Sample {}: {}'.format(i, readable_actions))

    if state_structure:
        print('State Space: {}'.format(env.observation_space))

    if step:
        print('Initial Render:')
        env.render(mode='human')
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print('State: \n{}'.format(observation))
        print('Turn Score: {}'.format(reward))
        print('Is Done: {}'.format(done))
        print('Info: {}'.format(info))
        print('Turn Render:')
        env.render(mode='human')


if __name__ == '__main__':
    args = parser.parse_args()
    action_encoding = args.action_encoding
    sample_actions = args.sample_actions
    state_structure = args.state_structure
    step = args.take_step
    check_evn(action_encoding, sample_actions, state_structure, step)
