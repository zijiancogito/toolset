#!/usr/bin/python3
import sys
import re
import os
import argparse
from collections import Counter
from utils.Parser import Rules

import pdb

class AsmBlock:
  def __init__(self, filename):
    self.filename = filename

  @property
  def simple_label(self):
    return self._label_sentence()

  def all_samples(self, out):
    label_list = []
    with open(self.filename, 'r') as f:
      line = f.readline()
      while line:
        # pdb.set_trace()
        tmp_list = line.strip().split(";")
        for sentence in tmp_list[:-1]:
          write_to_file(out, parser_code(sentence.strip())+'\t'+'0')

        write_to_file(out, parser_code(tmp_list[-1].strip())+'\t'+'1')
        line = f.readline()

  def _label_sentence(self):
    label_dict = {}
    pos = 0
    neg = 0
    with open(self.filename, 'r') as f:
      line = f.readline()
      while line:
        # pdb.set_trace()
        tmp_list = line.strip().split(";")
        for sentence in tmp_list[:-1]:
          try:
            label_dict[parser_code(sentence.strip())].append(0)
          except:
            label_dict[parser_code(sentence.strip())] = [0]
        try:
          label_dict[parser_code(tmp_list[-1].strip())].append(1)
        except:
          label_dict[parser_code(tmp_list[-1].strip())] = [1]
        line = f.readline()
    return label_dict

  def block_features(self):
    


def max_probability(dic):
  for key in dic:
    counts = Counter(dic[key])
    top = counts.most_common(1)
    dic[key] = top[0][0]
  return dic

def dict_to_stream(dic):
  tmp_list = [ "%s\t%s" % (re.sub('\t', ' ', item), str(dic[item])) for item in dic ]
  return "\n".join(tmp_list)

def write_to_file(out, ostream):
  out.write(ostream)
  out.write('\n')

def parser_code(code, code_type='asm'):
  parser = Rules(code_type, code)
  return parser.pcode.strip()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Label asm border')
  parser.add_argument(dest='filenames',metavar='filename', nargs='*')
  parser.add_argument('-m', dest='mode', action='store',
                            choices={'pure','simle','full'}, default='full',
                            help='')
  parser.add_argument('-o', dest='outfile', action='store', required=True, help='output file')
  args = parser.parse_args()

  ofstream = open(args.outfile, 'w+')
  if args.mode == 'simple':
    for filename in args.filenames:
      labels = AsmBlock(filename)
      stream = dict_to_stream(max_probability(labels.simple_label))
      write_to_file(ofstream, stream)
  elif args.mode == 'full':
    for filename in args.filenames:
      labels = AsmBlock(filename)
      labels.all_samples(ofstream)
  ofstream.close()