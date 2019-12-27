import os
import subprocess
import sys
from utils.listdir import list_all_files
from multiprocessing import Pool
obj_dir = sys.argv[2]

def process(filename):
    basename, extension = os.path.splitext(os.path.basename(filename))
    # cmd = "g++ -std=c++11 "+filename
    cmd = "g++ -std=c++11 -g "+filename+" -o " + obj_dir +basename+" -lm"
    print(cmd)
    obj = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True) 
    cmd_error = obj.stderr.read()
    obj.stderr.close()
    obj.stdout.close()
    if "error" in cmd_error:
        rm = "mv "+filename+" ../fail/"
        subprocess.run(rm, shell=True,universal_newlines=True)
        
files = list_all_files(sys.argv[1])
if __name__ == '__main__':
    with Pool(30) as p:
        p.map(process, files)