#!/usr/bin/python3
import os
import sys
from utils.listdir import list_all_files
from utils.Parser import Rules
from multiprocessing import Pool

sourcePath = sys.argv[1]
tar_dir = sys.argv[2]

def process(filename):
    basename = os.path.basename(filename)
    print(filename)
    sourceParser = open(tar_dir+basename, 'w')
    codefile = open(filename,'r')
    code = codefile.read().split('\n')
    for i in code:
        if i == "":
            continue
        j = i.split('\t')[1]
        parser = Rules('cpp',j)
        sourceParser.write(i.split('\t')[0]+'\t')
        sourceParser.write(parser.pcode.strip())
        sourceParser.write('\n')
    sourceParser.close()
    codefile.close()

filelist = list_all_files(sourcePath)
if __name__ == '__main__':
    with Pool(30) as p:
        p.map(process, filelist)