from utils.listdir import list_all_files
import sys

# get headers and user's code from sourcecode
# python3 dHeaders.py [source_code_dir] [code_dir] [header_dir]

# source code
#   #inlcude xxx
#   #include xxx
#   code line

# code
#   empty line [header]
#   empty line [header]
#   code line

# header
#   #include xxx
#   #include xxx
#   empty line [code line]

root_dir = sys.argv[1]
tar_dir = sys.argv[2]
header_dir = sys.argv[3]
files = list_all_files(root_dir)

for filename in files:
    print(filename)
    out = open(filename.replace(root_dir, tar_dir), 'w')
    header = open(filename.replace(root_dir, header_dir), 'w')
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            if line.startswith('#include'):
                header.write(line)
                out.write('\n')
            else:
                #print(line)
                out.write(line)
                header.write('\n')
            line = f.readline()
    out.close()
    header.close()
