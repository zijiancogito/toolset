import re
import os
import sys
from extrfiles import *
import pdb


extract_dir = '../../DataSets/ccode/extract/'      #sys.argv[1]
target_c_file = os.path.join(extract_dir, 'extract_c.txt')
target_asm_file = os.path.join(extract_dir, 'extract_asm.txt')
target_context_file = os.path.join(extract_dir, 'extract_context.txt')

asm_dir = "../../DataSets/ccode/p1/asm/"

def insnMap(cfg_func):
    insn_map = {}
    for cfg_node in cfg_func.cfg_nodes:
        insn_string_list = cfg_node.node_asm_body.split('\n')
        for insn_string in insn_string_list:
            insn = insn_string.split(':')[1].strip()
            addr = insn_string.split(':')[0].strip()
            insn_map[addr] = insn
    return insn_map

def extrAsm(asm_file):
    asm_dict = {}
    with open(asm_file, 'r') as f:
        for line in f.readlines():
            func_name = line.strip().split(':\t')[0]
            func_body = line.strip().split(':\t')[1]
            asm_dict[func_name] = func_body
    return asm_dict

def extrCandASM(yaml_file):
    basename, extention = os.path.splitext(os.path.basename(yaml_file))
    print(basename)
    asm_dict = extrAsm(os.path.join(asm_dir, basename+'.s'))
    #print(asm_dict)
    binCustom = CFG_Bin_Custom()
    binCustom.load_yaml_file(yaml_file)
    c_string_list = []
    asm_string_list = []
    context_string_list = []
    for cfg_func in binCustom.cfg_funcs:
        func_name = cfg_func.funcName
        insn_map = insnMap(cfg_func)
        for cfg_node in cfg_func.cfg_nodes:
            context = asm_dict[func_name]
            if cfg_node.node_c_body != 'NULL\n':
                # pdb.set_trace()
                c_list = cfg_node.node_c_body.split('\n')
                for item in c_list:
                    if item.startswith("#"):
                        c_list.remove(item)
                c_body_string = cBlock2String(' '.join(c_list))
                if len(c_body_string):
                    c_string_list.append(c_body_string)
                    asm_string_list.append(asmBlock2String(cfg_node.node_asm_body))
                    context_string_list.append(context)
    return c_string_list, asm_string_list, context_string_list

def cBlock2String(c_block):
    tmp_string = re.sub(r'[{}]', '', c_block)
    return ' '.join(tmp_string.split())

def asmBlock2String(asm_block):
    asm_block_without_addr = re.sub(r'0x[0-9a-fA-F]+:', ' ', asm_block)
    tmp_string = re.sub(r'\n', ' ;', asm_block_without_addr) + ' ;'
    return ' '.join(tmp_string.split())

def process(dir):
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    t_c_file = open(target_c_file, 'w')
    t_a_file = open(target_asm_file, 'w')
    t_con_file = open(target_context_file, 'w')
    count = 0
    for yaml_file in os.listdir(dir):
        if yaml_file.endswith('.yaml'):
            c_string_list, asm_string_list, context_string_list = extrCandASM(os.path.join(dir, yaml_file))
            for c_string in c_string_list:
                t_c_file.write(c_string + '\n')
            for asm_string in asm_string_list:
                t_a_file.write(asm_string + '\n')
            for context_string in context_string_list:
                t_con_file.write(context_string + '\n')
        count += 1
        print(count,':',yaml_file)
    t_c_file.close()
    t_a_file.close()
    t_con_file.close()

if __name__ == '__main__':
    process(sys.argv[1])