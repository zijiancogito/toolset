import os
import subprocess
import sys
from utils.listdir import list_all_files
from utils.tools import clang_dir, clangpp_dir, print_function_names_lib_dir

plugin_option = "-plugin print-fns"
load_option = "-cc1 -load"
source_code_dir = sys.argv[1]
out_dir = sys.argv[2]

files = list_all_files(source_code_dir)
function_list_file = open("functions.txt", 'w')
for file in files:
    if file[-2:] == '.c' or file[-2:] == '.h':
        cmd = clang_dir+" "+load_option+" "+print_function_names_lib_dir+" "+plugin_option+" "+'\"'+file+'\"'
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()
        cmd_error = obj.stderr.read()
        obj.stderr.close()
        function_list_file.write("file: "+file+'\n'+cmd_out+'\n')
    elif file[-4:] == '.cpp' or file[-3:] == '.cc' or file[-4:] == '.hpp':
        cmd = clangpp_dir+" "+load_option+" "+print_function_names_lib_dir+" "+plugin_option+" "+'\"'+file+'\"'
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()
        cmd_error = obj.stderr.read()
        obj.stderr.close()
        function_list_file.write("file: "+file+'\n'+cmd_out+'\n')
    else:
        pass

function_list_file.close()  