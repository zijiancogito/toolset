import os
import subprocess
import sys
from utils.listdir import list_all_files

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

# Compile these codes and remove failed.
# python3 pre.py [dir]
# files = list_all_files(sys.argv[1])
# fail = sys.argv[2]
# for filename in files:
#         cmd = "clang++ "+filename
#         print(cmd)
#         obj = subprocess.run(cmd, shell=True,universal_newlines=True)
#         if obj.returncode == 1:
#                 mv = "mv '"+filename+"' '"+fail+"'"
#                 print(mv)
#                 subprocess.run(mv, shell=True,universal_newlines=True)

# Delete Comment
# python3 pre.py [dir]
# files = list_all_files(sys.argv[1])
# out_dir = sys.argv[2]
# for filename in files:
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

# files = list_all_files(sys.argv[1])
# out_dir = sys.argv[2]
# for filename in files:
#         basename, extension = os.path.splitext(os.path.basename(filename))
#         cmd = "gcc -S -g " + filename + " -o "+out_dir+basename+".s"
#         print(cmd)
#         obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)

# filename
# files = list_all_files(sys.argv[1])
# print(len(files))
# count = 0
# for filename in files:
#         count += 1
#         cmd = "mv '"+filename+"' '"+filename+".cpp'"
#         print(str(count)+'/'+str(len)+'\t'+cmd)
#         obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)

#
files = list_all_files(sys.argv[1])
out_dir = sys.argv[2]
num = len(files)
count = 0
for filename in files:
    count += 1
    print(str(count)+'/'+str(num)+"\t"+filename)
    basename = os.path.basename(filename)
    f = open(filename, 'r')
    line = f.readline()
    out = open(out_dir+basename,'w')
    while line:
        if basename in line:
            pass
        else:
            out.write(line)
        line = f.readline()
    f.close()
    out.close()
