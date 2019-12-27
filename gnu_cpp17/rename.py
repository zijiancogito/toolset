import os
import sys
import subprocess
from utils.listdir import list_all_files
from multiprocessing import Pool
# rename source code files
#python3 rename.py [yaml_file_dir] [code_file_dir]

yaml_dir = sys.argv[1]
code_dir = sys.argv[2]
fail_dir = sys.argv[3]
def process(filename):
    try:
        if filename.endswith('.c') or filename.endswith('.cpp'):
            #print(filename)
            basename, extension = os.path.splitext(os.path.basename(filename))
            yaml = yaml_dir+basename+'.yaml'
            cmd = "clang-rename --extra-arg-before='-std=c++11' -i --input='"+yaml+"' '"+filename+"'"
            print(cmd)
            obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            obj.stdout.close()
            cmd_error = obj.stderr.read()
            obj.stderr.close()
        else:
            pass
    except:
        mv = "mv '"+filename+"' '"+fail_dir+"'"
        subprocess.run(mv, shell=True,universal_newlines=True)

#yamls = list_all_files(yaml_dir)
files = list_all_files(code_dir)
if __name__ == '__main__':
    with Pool(30) as p:
        p.map(process, files)