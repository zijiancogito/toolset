#!/usr/bin/python3
from sklearn.model_selection import train_test_split
import argparse
import os

def split_data(asm_file, c_file, test_size):
  asm_f = open(asm_file, 'r')
  c_f = open(c_file, 'r')
  asm = asm_f.readlines()
  c = c_f.readlines()
  x_train, x_test, y_train, y_test = train_test_split(asm, c, test_size=test_size)
  del asm, c
  asm_f.close()
  c_f.close()
  return x_train, x_test, y_train, y_test

def write(ofile, olist):
  with open(ofile, 'w') as out:
    out.write(''.join(olist))

INPUT_TEST_FILE = "inputs.test.txt"
TARGETS_TEST_FILE = "targets.test.txt"
INPUT_TRAIN_FILE = "inputs.train.txt"
TARGETS_TRAIN_FILE = "targets.train.txt"

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Split datasets')
  parser.add_argument('-c', dest='cfile', action='store', required=True)
  parser.add_argument('-s', dest='asmfile', action='store', required=True)
  parser.add_argument('-o', dest='outdir', action='store', default='./')
  parser.add_argument('--size', dest='test_size', action='store', default=0.0001)
  args = parser.parse_args()

  inputs_train, inputs_test, targets_train, targets_test = split_data(args.asmfile, args.cfile, args.test_size)

  write(os.path.join(args.outdir, INPUT_TEST_FILE), inputs_test)
  write(os.path.join(args.outdir, TARGETS_TEST_FILE), targets_test)
  write(os.path.join(args.outdir, INPUT_TRAIN_FILE), inputs_train)
  write(os.path.join(args.outdir, TARGETS_TRAIN_FILE), targets_train)

  del inputs_test, inputs_train, targets_test, targets_train

