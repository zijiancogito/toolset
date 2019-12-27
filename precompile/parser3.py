#!/usr/bin/python3
import os
from extractCode import Code

path = "/home/jho/Leetcode/workspace/asm/"
# sourcePath = "/home/jho/Leetcode/workspace/extractResult/source.txt"
# asmPath = "/home/jho/Leetcode/workspace/extractResult/asm.txt"
# fail = open("/home/jho/Leetcode/workspace/extractResult/fail.txt", 'w')
# success = open("/home/jho/Leetcode/workspace/extractResult/success.txt", 'w')

# sourcePath = "/home/jho/Leetcode/workspace/extractResult/source1.txt"
# asmPath = "/home/jho/Leetcode/workspace/extractResult/asm1.txt"
# fail = open("/home/jho/Leetcode/workspace/extractResult/fail1.txt", 'w')
# success = open("/home/jho/Leetcode/workspace/extractResult/success1.txt", 'w')

sourcePath = "/home/jho/Leetcode/workspace/extractResult/source2.txt"
asmPath = "/home/jho/Leetcode/workspace/extractResult/asm2.txt"
fail = open("/home/jho/Leetcode/workspace/extractResult/fail2.txt", 'w')
success = open("/home/jho/Leetcode/workspace/extractResult/success2.txt", 'w')

filelist = os.listdir(path)
sourceParser = open(sourcePath, 'w')
asmParser = open(asmPath, 'w')
count = 0
for filename in filelist:
    try:
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
    except:
        fail.write(filename)
        fail.write('\n')
    finally:
        pass

# for filename in filelist:
#     code = Code(path + filename).codemap
#     for pair in code:
#         sourceParser.write(str(pair[1]))
#         sourceParser.write('\n')
#         asmParser.write(str(pair[2]))
#         asmParser.write('\n')

sourceParser.close()
asmParser.close()
success.close()
fail.close()

