#!/usr/bin/python3
import os, sys
import json
import argparse

"""file to functions"""

def slice_functions(code, asm, res):
  if code == []:
    return res
  end = code.index('}')
  c_body = code

def function_process(cfile, asmfile):
  return

"""slice asm code as labels"""

def slice_asm(code, label, res):
  if 'True' not in label:
    if code != []:
      res.apppend(' ; '.join(code))
    return res
  end = label.index('True')
  res.append(' ; '.join(code[:end+1]))
  slice_asm(code[end+1:], label[end+1:], res)

def label_process(asmfile, labelfile):
  af = open(asmfile, 'r')
  lf = open(labelfile, 'r')
  code = af.read().strip().split('\n')
  label = lf.read().strip().split('\n')
  res = []
  slice_asm(code, label, res)
  return res

def write_list_to_file(ofile, lst):
  with open(ofile, 'w') as f:
    f.write('\n'.join(lst))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Label asm border')
  parser.add_argument(dest='filenames',metavar='filename', nargs='*')
  parser.add_argument('-m', dest='mode', action='store',
                            choices={'label','function'}, default='label',
                            help='')
  parser.add_argument('-o', dest='outfile', action='store', required=True, help='output file')
  parser.add_argument('-f', dest='file', action='store', required=True, help='')
  args = parser.parse_args()

  if args.mode == 'label':
    res = label_process(args.filenames[0], args.file)
    print(res)
    write_list_to_file(args.outfile, res)
