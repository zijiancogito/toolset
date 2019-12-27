
import os
import subprocess
from utils.listdir import list_all_files
from utils.tools import clang_functions_cfg

source_code_dir = "/Users/yingcao/re/DataSets/"
fileslist = list_all_files(source_code_dir)
outfile = open("function.cfg", 'w')
count=0
for file in fileslist:
    if file[-2:] == '.c' or file[-2:] == '.h' or file[-4:] == '.cpp' or file[-3:] == '.cc' or file[-4:] == '.hpp':
        cmd = clang_functions_cfg+' '+'\"'+file+'\"'
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()
        cmd_error = obj.stderr.read()
        obj.stderr.close()
        outfile.write("filename: "+file+'\n\n'+cmd_out+'\n')
        count = count + 1
    else:
        pass

print(count)