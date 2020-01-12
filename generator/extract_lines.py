#!/usr/bin/python3
import os, sys
import pdb
import yaml
from reasm import AsmParser, CParser
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
        if c_block != '{':
          asm_list.append(asm_block[addr])
      pdb.set_trace()
      asm = AsmParser(';'.join(asm_list))
      new_asm = asm.new_asm
      table = asm.imm_tab
      new_c = CParser(c_block).sub_table(table)


if __name__ == '__main__':
  files = list_all_files(sys.argv[1])
  for filename in files:
    read_file(filename)


