# -*- coding: utf-8 -*-
from pprint import pprint
import re
import sys
var_feat = r"var\d+"
fun_feat = r"func\d+"
source_feat = r" \*{4} (.*)"
asm_feat = r" [\t]+([^\.\t].*)"
director_feat = '[0-9]+(\\ )+(\\t)+\.'

'''
var_rename: rich var semantics
'''
def var_rename(stat):
    cnt = 1
    while True:
        r = re.search(var_feat, stat)
        if r == None: break
        n = "v" + str(cnt)
        stat = re.sub(r"\b"+r.group(0)+r"\b", n, stat)
        #print("full src:", stat)
        cnt += 1
    return stat

'''
TODO: functinon name line shouldn't match the asm_feat.
'''
def parse():
    with open(sys.argv[1], 'r') as f:
        lines = f.read().split('\n')
    cnt = 0
    src = ['']
    bare_src = ['']
    full_src = ['']
    asm = [[]]
    
    for line in lines:
        if line == '': # #include<...> and function declare
            continue
        if re.search(director_feat, line):
            continue
        src_search = re.search(source_feat, line)
        if src_search != None:
            tmp = src_search.group(1)
            if tmp == '{':
                tmp = src[-1]+tmp
            src.append(tmp)
            tmp = re.sub(fun_feat, "func", tmp)
            bare_tmp = re.sub(var_feat, "var", tmp)
            full_tmp = var_rename(tmp)

            bare_src.append(bare_tmp)
            full_src.append(full_tmp)
            asm.append([])
            
            cnt += 1
        elif cnt:
            asm_search = re.search(asm_feat, line)
            if asm_search != None:
                tmp = asm_search.group(1)
                if tmp.startswith('func') or tmp.startswith('main'): # bullshit
                    continue
                tmp = tmp.replace('\t', ' ')
                asm[cnt].append(tmp)
            else:
                #print("Ops: asm search not find")    
                pass
            #print(repr(tmp))
    '''
    for i in range(len(src)):
        pprint(src[i])
        pprint(bare_src[i])
        pprint(full_src[i])
        pprint(asm[i])
    '''
    src_f = open('ori_src.txt', 'w')
    src_bare_f = open('bare_src.txt', 'w')
    src_full_f = open('full_src.txt', 'w')
    asm_f = open('asm_lst.txt', 'w')
    for i in range(len(src)):
        if src[i] == '':
            continue
        if asm[i] == []: # note that sometimes no asm correspond with src.
            continue
        src_f.write(src[i]+'\n')
        src_bare_f.write(bare_src[i]+'\n')
        src_full_f.write(full_src[i]+'\n')
        _ = ';'.join(asm[i])
        asm_f.write(_+'\n')
    src_f.close()
    src_bare_f.close()
    src_bare_f.close()
    asm_f.close()

if __name__ == "__main__":
    parse()


    
