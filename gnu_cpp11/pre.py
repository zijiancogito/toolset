import os
import subprocess
import sys
from utils.listdir import list_all_files
from utils.tools import datapath
from multiprocessing import Pool
# Copy all c files to a new dir and rename these files
# python3 pre.py [source_dir] [tar_dir]
# files = list_all_files(sys.argv[1])
# tardir = sys.argv[2]
# cfiles = []
# for filename in files:
#     if filename.endswith('.c'):
#         cfiles.append(filename)
# count = 0
# for filename in cfiles:
#         cmd ="cp '"+filename+"' "+tardir+"code"+str(count)+'.c'
#         print(cmd)
#         obj = subprocess.Popen(cmd, shell=True,universal_newlines=True)
#         count = count + 1

""" 
    Compile these codes and remove failed.
    python3 pre.py [dir]
"""
# files = list_all_files(datapath+"src_n/")
# fail = datapath+"fail/"
# def process(filename):
#         cmd = "clang++ -std=c++11 "+filename
#         print(cmd)
#         obj = subprocess.run(cmd, shell=True,universal_newlines=True)
#         if obj.returncode == 1:
#                 mv = "mv '"+filename+"' '"+fail+"'"
#                 print(mv)
#                 subprocess.run(mv, shell=True,universal_newlines=True)
# if __name__ == '__main__':
#     with Pool(30) as p:
#         p.map(process, files)

"""
    Delete Comment
    python3 pre.py [dir]
"""
# files = list_all_files(datapath+"src_n/")
# out_dir = datapath + "src/"
# def process(filename):
#         cmd = "g++ -fpreprocessed -dD -E " + filename
#         print(cmd)
#         obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
#         cmd_out = obj.stdout.read()
#         obj.stdout.close()
#         cmd_error = obj.stderr.read()
#         obj.stderr.close()
#         code = cmd_out.split('\n')
#         for line in code:
#                 if filename in line:
#                         code.remove(line)
#         basename = os.path.basename(filename)
#         out = open(out_dir+basename,'w')
#         out.write("\n".join(code))
#         out.close()
# if __name__ == '__main__':
#     with Pool(30) as p:
#         p.map(process, files)

"""
    rename filename
    python3 pre.py [source code path]
"""
files = list_all_files(datapath+"src_n/")
def process(filename):
    cmd = "mv '"+filename+"' '"+filename+".cpp'"
    print(cmd)
    obj = subprocess.run(cmd, shell=True, universal_newlines=True)

if __name__ == '__main__':
    with Pool(30) as p:
        p.map(process, files)
