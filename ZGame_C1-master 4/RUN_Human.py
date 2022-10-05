import os
import argparse
from ZGameHumanPlay import ZGame
from gym_zgame.envs.Print_Colors.PColor import PBack, PFore, PFont, PControl

parser = argparse.ArgumentParser(description='CLI Argument Parser for Human Play.')
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
    data_log_file = args.outfile
    os.system('mode con: cols=125 lines=62')
    zgame_env = ZGame(data_log_file)
    zgame_env.run_gui()
