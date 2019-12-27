import os
import sys
import subprocess
import re
from utils.listdir import list_all_files

# get asm from binary files
# python3 dasm.py [binary files dir] [asm files dir]


bin_dir = sys.argv[1]
asm_dir = sys.argv[2]
files = list_all_files(bin_dir)

procount = 0
allnum=len(files)
for filename in files:
    print(str(procount) + "/"+ str(allnum) +"\t" +filename)
    procount +=1
    # Get symbol list
    sym_tab_cmd = "objdump -t "+"'"+filename+"'"
    basename, extension = os.path.splitext(os.path.basename(filename))
    obj = subprocess.Popen(sym_tab_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cmd_out = obj.stdout.read().strip().split('\n')
    obj.stdout.close()
    cmd_error = obj.stderr.read()
    obj.stderr.close()
    symbol_list = []
    # 00000000000006f8 g     F .init  0000000000000000              _init
    for i in cmd_out:
        tmp = list(filter(lambda x: x!='', i.split(' ')))
        if tmp:
            if len(tmp)==5:
                label = tmp[-2].split('\t')[0]
                name = tmp[-1]
                if label == '.text' and (name.startswith('Function') or name == 'main' ):
                    symbol_list.append(name)
    # Get asm
    asm_dict = {}
    asm_cmd = "objdump -d --section='.text' '"+filename+"'"
    obj = subprocess.Popen(asm_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cmd_out = obj.stdout.read().strip().split('\n\n')[6:]
    obj.stdout.close()
    cmd_error = obj.stderr.read()
    obj.stderr.close()
    asm_dict = {}
    for function in cmd_out:
        name = function.split('\n')[0].split(' ')[-1][1:-2]
        if name in symbol_list:
            asm_code = []
            for i in function.split('\n')[1:]:
                code = i.split('\t')[-1].split('#')[0].strip()
                asm_code.append(code)
            asm_dict[name] = asm_code
    # Out to file
    out = open(os.path.join(asm_dir, basename+'.s'), 'w')
    for i in asm_dict:
        out.write(i+':\t')
        asm_list = []
        for j in asm_dict[i]:
            asm_list.append(re.sub('\s', '', j))
        out.write(' '.join(asm_list) + '\n')

    # Out to one line
    """ out = open(asm_dir+basename+'.sl','w')
    for i in asm_dict:
        out.write(i+':\t')
        line = ''
        for j in asm_dict[i]:
            import pdb
            pdb.set_trace()
            line = line + ' ' + re.sub('\s','',j) 
        out.write(line)
        out.write('\n')
    out.close() """
