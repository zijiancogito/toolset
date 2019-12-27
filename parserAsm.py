#!/usr/bin/python3
import os
import sys
from utils.listdir import list_all_files
from utils.Parser import Rules

sourcePath = sys.argv[1]
tar_dir = sys.argv[2]
#filelist = list_all_files(sourcePath)
#count = 0
#num = len(filelist)
#for filename in filelist:
#print(str(count)+'/'+str(num)+'\t'+filename)
#basename = os.path.basename(filename)
sourceParser = open(tar_dir, 'w')
codefile = open(sourcePath,'r')
code = codefile.read().split('\n')
for i in code:
    if i == "":
        continue
    #j = i.split('\t')[1]
    parser = Rules('asm',i)
    sourceParser.write(parser.pcode.strip())
    sourceParser.write('\n')
sourceParser.close()
codefile.close()

