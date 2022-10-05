import argparse
from ZGameMachineTrain import ZGame

parser = argparse.ArgumentParser(description='CLI Argument Parser for RL Training.')
parser.add_argument('--modelfilename', help='Output file name for learned model.', default='rl-agent')
parser.add_argument('--training_steps', help='Number of steps to train for.', type=int, default=1000)
parser.add_argument('--num_envs', help='Number of parallel environments.', type=int, default=4)


if __name__ == '__main__':
    args = parser.parse_args()
    model_filename = args.modelfilename
    training_steps = args.training_steps
    num_envs = args.num_envs
    zgame_env = ZGame(model_filename=model_filename)
    zgame_env.run()
