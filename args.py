import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--team', type=int, default=8)
parser.add_argument('--level', type=int, default=4)
parser.add_argument('--seperation', type=int, default=2)
parser.add_argument('--time', type=int, default=4)

parser.add_argument('-l', '--show_level', action='store_true')
parser.add_argument('-t', '--show_team', action='store_true')
parser.add_argument('-m', '--show_meet', action='store_true')
args = parser.parse_args()