#!/usr/bin/python3
import os

path = "/home/jho/Leetcode/workspace/procomments/"
outpath = "/home/jho/Leetcode/workspace/purecode/"
sourceFiles = os.listdir(path)
for sourcefile in sourceFiles:
    with open(path+sourcefile) as f:
        count = 0
        try:
            out = open(outpath+sourcefile, 'w') 
            for line in f:
                if count == 0:
                    count = count + 1
                    continue
                else:
                    out.write(line)
            out.close()
        except:
            print(sourcefile)


