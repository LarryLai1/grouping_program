import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--team', type=int)
parser.add_argument('--level', type=int)
parser.add_argument('--seperation', type=int)
parser.add_argument('--time', type=int)
args = parser.parse_args()