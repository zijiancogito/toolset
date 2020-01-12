#!/usr/bin/python3
import os, sys
import pdb
import yaml
from reasm import AsmParser, CParser
sys.path.append('..')
from utils.listdir import list_all_files


def read_file(filename):
  print(filename)
  with open(filename, 'r') as f:
    stream = f.read()
    tmp = yaml.load(stream)
    #pdb.set_trace()
    basename, ext = os.path.split(os.path.basename(filename))
    cfile = os.path.join(os.path.dirname(filename), "list/%s.c", basename)
    sfile = os.path.join(os.path.dirname(filename), "list/%s.s", basename)
    cf = open(cfile, 'w')
    sf = open(sfile, 'w')
    for line in tmp:
      c_block = line[0]
      if c_block == '{' or c_block == '}':
        continue
      asm_block = line[1]
      asm_list = []
      for addr in asm_block:
        if c_block != '{':
          asm_list.append(asm_block[addr])
      #pdb.set_trace()
      asm = AsmParser(';'.join(asm_list))
      new_asm = asm.new_asm
      table = asm.imm_map
      c = CParser(c_block)
      new_c = c.sub_table(table)
      cf.write(new_c)
      cf.write('\n')
      sf.write(new_asm)
      sf.write('\n')
    cf.close()
    sf.close()


if __name__ == '__main__':
  files = list_all_files(sys.argv[1])
  for filename in files:
    read_file(filename)


