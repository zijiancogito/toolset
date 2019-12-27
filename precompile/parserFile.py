#!/usr/bin/python3
import os
from extractCode import Code

sourcePath = sys.argv[1]



# sourceParser = open(sourcePath, 'w')
# asmParser = open(asmPath, 'w')
count = 0
for filename in filelist:
    try:
        sourceParser = open(sourcePath + filename[0:len(filename)-1]+'cpp', 'w')
        asmParser = open(asmPath + filename, 'w')
        code = Code(path + filename).codemap
        for pair in code:
            if pair[2] == "" or pair[1] == "":
                continue
            sourceParser.write(str(pair[1]))
            sourceParser.write('\n')
            asmParser.write(str(pair[2]))
            asmParser.write('\n')
        print(filename)
        success.write(filename)
        success.write('\n')
        count = count + 1
        sourceParser.close()
        asmParser.close()
    except:
        fail.write(filename)
        fail.write('\n')
    finally:
        pass

success.close()
fail.close()

