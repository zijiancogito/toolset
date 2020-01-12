import os, sys
import pdb
import yaml
sys.path.append('..')
from utils.listdir import list_all_files

def read_file(filename):
  with open(filename, 'r') as f:
    stream = f.read()
    tmp = yaml.load(stream)
    pdb.set_trace()


if __name__ == '__main__':
  files = list_all_files(sys.argv[1])
  for filename in files:
    read_file(filename)


