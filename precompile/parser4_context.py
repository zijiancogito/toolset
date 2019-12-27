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

# sourcePath = "/home/jho/Leetcode/workspace/extractResult/source2.txt"
# asmPath = "/home/jho/Leetcode/workspace/extractResult/asm2.txt"
# fail = open("/home/jho/Leetcode/workspace/extractResult/fail2.txt", 'w')
# success = open("/home/jho/Leetcode/workspace/extractResult/success2.txt", 'w')

# sourcePath = "/home/jho/Leetcode/workspace/Result/cpp/"
# asmPath = "/home/jho/Leetcode/workspace/Result/asm/"

cppTestPath = "/home/jho/Leetcode/workspace/extractResult/sourceTest_context.txt"
asmTestPath = "/home/jho/Leetcode/workspace/extractResult/asmTest_context.txt"
cppTrainPath = "/home/jho/Leetcode/workspace/extractResult/sourceTrain_context.txt"
asmTrainPath = "/home/jho/Leetcode/workspace/extractResult/asmTrain_context.txt"
cppVerifyPath = "/home/jho/Leetcode/workspace/extractResult/sourceVerify_context.txt"
asmVerifyPath = "/home/jho/Leetcode/workspace/extractResult/asmVerify_context.txt"

fail = open("/home/jho/Leetcode/workspace/extractResult/fail3.txt", 'w')
success = open("/home/jho/Leetcode/workspace/extractResult/success3.txt", 'w')

filelist = os.listdir(path)
cppTrain = open(cppTrainPath, 'w')
asmTrain = open(asmTrainPath, 'w')
cppTest = open(cppTestPath, 'w')
asmTest = open(asmTestPath, 'w')
cppVerify = open(cppVerifyPath, 'w')
asmVerify = open(asmVerifyPath, 'w')
count = 0
train = 73627
test = 21036 + 73627
verify = 10519
for filename in filelist:
    try:
        code = Code(path + filename).codemap
        for pair in code:
            if pair[2] == "" or pair[1] == "":
                continue
            if pair[2] == "\n" or pair[1] == "\n":
                continue
            if count <= train:
                cppTrain.write(str(pair[1]))
                cppTrain.write('\n')
                asmTrain.write(str(pair[2]))
                asmTrain.write('\n')
            elif count > train and count <= test:
                cppTest.write(str(pair[1]))
                cppTest.write('\n')
                asmTest.write(str(pair[2]))
                asmTest.write('\n')
            else:
                cppVerify.write(str(pair[1]))
                cppVerify.write('\n')
                asmVerify.write(str(pair[2]))
                asmVerify.write('\n')
        print(filename)
        success.write(filename)
        success.write('\n')
        #count = count + 1
        if count <= train:
            cppTrain.write('\n')
            asmTrain.write('\n')
        elif count > train and count <= test:
            cppTest.write('\n')
            asmTest.write('\n')
        else:
            cppVerify.write('\n')
            asmVerify.write('\n')
 
    except:
        fail.write(filename)
        fail.write('\n')
    finally:
        pass
    count = count + 1

# for filename in filelist:
#     code = Code(path + filename).codemap
#     for pair in code:
#         sourceParser.write(str(pair[1]))
#         sourceParser.write('\n')
#         asmParser.write(str(pair[2]))
#         asmParser.write('\n')
cppTest.close()
cppTrain.close()
cppVerify.close()
asmTest.close()
asmTrain.close()
asmVerify.close()

success.close()
fail.close()

