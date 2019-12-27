#!/usr/bin/python3
import os
import sys
import argparse

def build_lst(code_file, label_file):
  code_f = open(code_file, 'r')
  label_f = open(label_file, 'r')
  code = code_f.readline()
  label = label_f.readline()
  lst = []
  while code and label:
    code = code.strip()
    label = label.strip()
    lst.append((code, label))
    code = code_f.readline()
    label = label_f.readline()
  code_f.close()
  label_f.close()
  return lst

def lst_to_stream(lst):
  stream_lst = []
  for pair in lst:
    stream_lst.append(pair[0]+'\t'+pair[1])
  return "\n".join(stream_lst)

def write(ofile, ostream):
  with open(ofile, 'w') as f:
    f.write(ostream)
    f.write('\n')


if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Split datasets')
  parser.add_argument('-c', dest='codefile', action='store', required=True)
  parser.add_argument('-l', dest='labelfile', action='store', required=True)
  parser.add_argument('-o', dest='outfile', action='store', required=True)
  args = parser.parse_args()
  write(args.outfile, lst_to_stream(build_lst(args.codefile, args.labelfile)))
  