# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import re
from utils.listdir import list_all_files
import yaml

# get asm from binary files
# python3 objdump.py [binary files dir] [yaml files dir]


bin_dir = sys.argv[1]
asm_dir = sys.argv[2]
files = list_all_files(bin_dir)

procount = 0
allnum=len(files)

for filename in files:
    if filename.endswith('.c') or filename.endswith("Makefile") or filename.endswith(".yaml"):
        continue
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
    asm_cmd = "objdump -d -S --section='.text' '"+filename+"'"
    obj = subprocess.Popen(asm_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cmd_out = obj.stdout.read()
    cmd_out = cmd_out.strip().split('\n\n')[6:]
    obj.stdout.close()
    cmd_error = obj.stderr.read()
    obj.stderr.close()
    asm_dict = {}
    for function in cmd_out:
        name = function.split('\n')[0].split(' ')[-1][1:-2]
        if name in symbol_list:
            asm_code = []
            flag = []
            for i in function.split('\n')[1:]:
                if len(i.strip().split('\t'))>1:
                    code = i.strip().split('\t')[-1].split('#')[0].strip()+'\n'
                    flag.append(1)
                else:
                    code = i+'\n'
                    flag.append(0)
                asm_code.append(code)
            asm_dict[name] = [asm_code, flag]
    # Out to file
    out = open(asm_dir+basename+'.yaml','w')
    out_dict = {}
    for i in asm_dict:
        source = ""
        asm = ""
        for j in range(len(asm_dict[i][-1])):
            if asm_dict[i][-1][j] == 0:  # is source code
                source += asm_dict[i][0][j]
                asm += "EMPTYLINE\n"
            else:
                source += "EMPTYLINE\n"
                asm += asm_dict[i][0][j]
        source_list = source.split("EMPTYLINE\n")
        asm_list = asm.split("EMPTYLINE\n")
        pair_list = []
        s_list = []
        a_list = []
        for j in source_list:
            if j == '':
                pass
            else:
                s_list.append(j)
        for j in asm_list:
            if j=='':
                pass
            else:
                a_list.append(j)
        if(len(a_list) < len(s_list)):
            a_list.append('\n')
        for j in range(len(s_list)):
            pair_list.append([s_list[j],a_list[j]])
        out_dict[i] = pair_list
    out.write(yaml.dump(out_dict))
    out.close()
