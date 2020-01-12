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
    for line in tmp:
      c_block = line[0]
      asm_block = line[1]
      asm_list = []
      for addr in asm_block:
        asm_list.append(addr)
      


if __name__ == '__main__':
  files = list_all_files(sys.argv[1])
  for filename in files:
    read_file(filename)


