import os
import argparse
from ZGameMachinePlay import ZGame

parser = argparse.ArgumentParser(description='CLI Argument Parser for Machine Playback.')
parser.add_argument('--model', help='Input file name for learned model.', default='rl-agent_2.5ishM')
parser.add_argument('--outfile', help='Data logging file name.', default='data_log.json')
parser.add_argument('--creation', help='Allow creation of output file.', default=False, action='store_true')


def validate_data(out_file, allow_creation=False):
    if allow_creation and not os.path.exists(out_file):
        f = open(out_file, 'w+')
        f.close()
    if not os.path.isfile(out_file):
        raise EnvironmentError('Bad filename provided in CLI arguments.')


if __name__ == '__main__':
    args = parser.parse_args()
    validate_data(args.outfile, allow_creation=args.creation)
    model_name = args.model
    data_log_file = args.outfile
    os.system('mode con: cols=125 lines=50')
    zgame_env = ZGame(model_filename=model_name, data_log_file=data_log_file)
    zgame_env.run()
