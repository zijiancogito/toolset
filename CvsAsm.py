import os
import subprocess
import sys
from utils.listdir import list_all_files

# map code and asm
# python3 CvsAsm.py [code_line_dir] [asm_line_dir] [out file]

code_dir = sys.argv[1]
asm_dir = sys.argv[2]
out = sys.argv[3]

files = list_all_files(asm_dir)
cout = open(out+'.cpp','w')
sout = open(out+'.s','w')
for filename in files:
    basename, extension = os.path.splitext(os.path.basename(filename))
    print(basename)
    asm_file = open(filename,'r')
    code_file = open(code_dir+basename+'.cpp','r')
    map_dic = {}
    for line in code_file:
        function_name = line[0:line.index(':')]
        map_dic[function_name] = [line[line.index('\t'):].strip()]
    for line in asm_file:
        function_name = line[0:line.index(':')]
        map_dic[function_name].append(line[line.index('\t'):].strip())
    asm_file.close()
    code_file.close()
    for k in map_dic:
        if len(map_dic[k])>1:
            cout.write(map_dic[k][0]+'\n')
            sout.write(map_dic[k][1]+'\n')

cout.close()
sout.close()
