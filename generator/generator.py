#!/usr/bin/python3
import os
import sys
import argparse
from collections import Counter

sys.path.append('../')
from utils.Parser import Rules

import pdb

def pure(asm_filename, c_filename, parser=True):
  """
  Same ASM to same C code

  """
  asm_f = open(asm_filename, 'r')
  c_f = open(c_filename, 'r')
  dic = {}
  asm_line = asm_f.readline()
  c_line = c_f.readline()
  while asm_line and c_line:
    if parser:
      asm = Rules('asm', asm_line.strip()).pcode.strip()
      c = Rules('cpp', c_line.strip()).pcode.strip()
    else:
      asm = asm_line.strip()
      c = c_line.strip()
    try:
      dic[asm].append(c)
    except:
      dic[asm] = [c]
    asm_line = asm_f.readline()
    c_line = c_f.readline()
  asm_f.close()
  c_f.close()
  return max_appearence(dic)

def max_appearence(dic):
  for asm in dic:
    counts = Counter(dic[asm])
    top = counts.most_common(1)
    dic[asm] = top[0][0]
  return dic

def simple(asm_filename, c_filename, parser=True):
  asm_f = open(asm_filename, 'r')
  c_f = open(c_filename, 'r')
  lst = []
  asm_line = asm_f.readline()
  c_line = c_f.readline()
  while asm_line and c_line:
    if parser:
      asm = Rules('asm', asm_line.strip()).pcode.strip()
      c = Rules('cpp', c_line.strip()).pcode.strip()
    else:
      asm = asm_line.strip()
      c = c_line.strip()
    lst.append((asm, c))
    asm_line = asm_f.readline()
    c_line = c_f.readline()
  asm_f.close()
  c_f.close()
  return list(set(lst))

def full(asm_filename, c_filename, oasm, oc, parser=True):
  asm_f = open(asm_filename, 'r')
  c_f = open(c_filename, 'r')
  asm_line = asm_f.readline().strip()
  c_line = c_f.readline().strip()
  while asm_line and c_line:
    if c_line =='}':
      pass
    else:
      if parser:
        write(oasm, Rules('asm', asm_line.strip()).pcode.strip())
        write(oc, Rules('cpp', c_line.strip()).pcode.strip())
      else:
        write(oasm, asm_line.strip()+'\n')
        write(oc, c_line.strip()+'\n')
    asm_line = asm_f.readline().strip()
    c_line = c_f.readline().strip()
  asm_f.close()
  c_f.close()

  

def dic_to_streams(dic):
  key_list = []
  val_list = []
  for key in dic:
    key_list.append(key)
    val_list.append(dic[key])
  key_stream = '\n'.join(key_list)
  val_stream = '\n'.join(val_list)
  return key_stream, val_stream

def lst_to_streams(lst):
  lst1, lst2 = [], []


def write(ofile, ostream):
  ofile.write(ostream)
  ofile.write('\n')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Mix codes')
  parser.add_argument(dest='filenames',metavar='filename', nargs='*')
  parser.add_argument('-o', dest='outfile', action='store', required=True, help='output file')
  parser.add_argument('-m', dest='mode', action='store',
                            choices={'pure','simle','full'}, default='pure',
                            help='')
  # parser.add_argument('-p', dest='parser', action='parser',
  #                           choices={True, False}, default=True,
  #                           help='')
  parser.add_argument('-l', dest='language', choices={'c','cpp'}, default='c')
  args = parser.parse_args()

  oasm = open("%s.%s"%(args.outfile, 's'), 'w')
  oc = open("%s.%s"%(args.outfile, args.language), 'w')
  if args.mode == 'pure':
    for filename in args.filenames:
      print(filename)
      dic = pure(filename+'.s', "%s.%s"%(filename, args.language))
      asm_stream, c_stream = dic_to_streams(dic)
      del dic
      write(oasm, asm_stream)
      del asm_stream
      write(oc, c_stream)
      del c_stream
  elif args.mode == 'simple':
    for filename in args.filenames:
      lst = simple(filename+'.s', "%s.%s"%(filename, args.language))
  elif args.mode == 'full':
    for filename in args.filenames:
      full("%s.%s"%(filename,'s'), "%s.%s"%(filename,args.language), oasm, oc)

  oasm.close()
  oc.close()