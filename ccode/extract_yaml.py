import os
import sys
import yaml
import pdb

_DATA_DIR = ["/home/jho/re/re/DataSets/",
             ["ccode/extract_yaml/"
             ]]

pdb.set_trace()

data_dirs = [os.path.join(_DATA_DIR[0], item) for item in _DATA_DIR[1]]
out_dirs = [os.path.split(item) for item in data_dirs]
files = []
for x in data_dirs:
  files.extend([os.path.join(x, filename) for filename in os.listdir(x)])
pdb.set_trace()

streams = [open(filename, 'r') for filename in files]

pdb.set_trace()
for stream in streams:
  data = yaml.load(stream)
  output = yaml.dump(data)
  functions = list(data["cfg_funcs"])
  for function in functions:
    nodes = list(data["cfg_funcs"][function]["cfg_nodes"])
    for node in nodes:
      asm_code = data["cfg_funcs"][function]["cfg_nodes"][node]["node_asm_body"]
      c_code = data["cfg_funcs"][function]["cfg_nodes"][node]["node_c_body"]

pdb.set_trace()
