import os
import subprocess
import sys
from utils.listdir import list_all_files
from utils.tools import clang_dir, clangpp_dir, print_function_names_lib_dir

# translate every function to a line
# python3 code2line.py [source code dir] [out code dir]

plugin_option = "-plugin print-fns"
load_option = "-cc1 -load"
source_code_dir = sys.argv[1]
out_dir = sys.argv[2]

files = list_all_files(source_code_dir)
for file in files:
    print(file+"\tCode2line!")
    cmd = clang_dir+" "+load_option+" "+print_function_names_lib_dir+" "+plugin_option+" "+'\"'+file+'\"'
    obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cmd_out = obj.stdout.read().strip().split('\n')
    obj.stdout.close()
    cmd_error = obj.stderr.read()
    obj.stderr.close()
    basename = os.path.basename(file)
    out = open(out_dir+basename,'w')
    for i in cmd_out:
        name = i.split(' ')[-1]
        func_cmd = "clang-check --ast-print --ast-dump-filter='"+name+"' '"+file+"'"
        func_obj = subprocess.Popen(func_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        func_cmd_out = func_obj.stdout.read()
        func_obj.stdout.close()
        func_cmd_error = func_obj.stderr.read()
        func_obj.stderr.close()
        tmp = func_cmd_out.split("Printing ")
        for j in tmp:
            if j.startswith(name+':'):
                code_list = j.strip().split('\n')[1:]
                code = ""
                for k in code_list:
                    code = code + " " + k.strip()
                out.write(name+":\t"+code)
                out.write('\n')
    out.close()
