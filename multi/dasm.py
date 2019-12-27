import os
import sys
import subprocess
import re
from utils.listdir import list_all_files
from multiprocessing import Pool
from utils.tools import clang_dir, clangpp_dir, print_function_names_lib_dir
# get asm from binary files
# python3 dasm.py [binary files dir] [asm files dir]

src_dir = sys.argv[1]
bin_dir = sys.argv[2]
asm_dir = sys.argv[3]

plugin_option = "-plugin print-fns"
load_option = "-cc1 -load"

# def getname(basename):
#     filename = src_dir + basename +".cpp"
#     cmd = "clang "+load_option+" "+print_function_names_lib_dir+" "+plugin_option+" "+'\"'+filename+'\"'
#     obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#     cmd_out = obj.stdout.read().strip().split('\n')
#     obj.stdout.close()
#     cmd_error = obj.stderr.read()
#     obj.stderr.close()
#     namelist = []
#     for i in cmd_out:
#         name = i.split(' ')[-1]
#         namelist.append(name)
#     return namelist

def process(filename):
    # Get symbol list
    sym_tab_cmd = "objdump -t --section='.text' " + "'" + filename+"'"
    print(sym_tab_cmd)
    basename, extension = os.path.splitext(os.path.basename(filename))
    obj = subprocess.Popen(sym_tab_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cmd_out = obj.stdout.read().strip().split('\n')
    obj.stdout.close()
    cmd_error = obj.stderr.read()
    obj.stderr.close()
    symbol_list = []

    # 00000000000006f8 g     F .init  0000000000000000              _init
    srcname = src_dir + basename +".cpp"
    namecmd = "clang++ "+load_option+" "+print_function_names_lib_dir+" "+plugin_option+" "+'\"'+srcname+'\"'
    print(namecmd)
    nameobj = subprocess.Popen(namecmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    name_cmd_out = nameobj.stdout.read().strip().split('\n')
    nameobj.stdout.close()
    name_cmd_error = nameobj.stderr.read()
    nameobj.stderr.close()
    namelist = []
    for i in name_cmd_out:
        fname = i.split(' ')[-1]
        namelist.append(fname)
    # print(namelist)
    for i in cmd_out:
        tmp = list(filter(lambda x: x!='', i.split(' ')))
        if tmp:
            if len(tmp)==5:
                label = tmp[-2].split('\t')[0]
                name = tmp[-1]
                filt = "c++filt "+name
                filtobj = subprocess.Popen(filt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                filt_out = filtobj.stdout.read()
                filtobj.stdout.close()
                filt_error = filtobj.stderr.read()
                nameobj.stderr.close()
                qname = filt_out.strip().split('(')[0]
                if label == '.text' and (qname in namelist):
                    symbol_list.append(qname)
                    # print(qname)
    # Get asm
    asm_dict = {}
    asm_cmd = "objdump -d --section='.text' '"+filename+"'"
    print(asm_cmd)
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
    # out = open(asm_dir+basename+'.s','w')
    # for i in asm_dict:
    #     out.write(i+':\n')
    #     for j in asm_dict[i]:
    #         out.write(j+'\n')
    #     out.write('\n')

    # Out to one line
    out = open(asm_dir+basename+'.sl','w')
    for i in asm_dict:
        out.write(i+':\t')
        line = ''
        for j in asm_dict[i]:
            line = line + ' ' + re.sub('\s','',j) 
        out.write(line)
        out.write('\n')
    out.close()

files = list_all_files(bin_dir)
if __name__ == '__main__':
    with Pool(1) as p:
        p.map(process, files)