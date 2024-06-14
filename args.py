import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--team', type=int)
parser.add_argument('--level', type=int)
parser.add_argument('--seperation', type=int)
parser.add_argument('--time', type=int)

parser.add_argument('--show_level', type=bool)
parser.add_argument('--show_team', type=bool)
parser.add_argument('--show_meet', type=bool)
args = parser.parse_args()