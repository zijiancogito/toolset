import sys
import time
import cfile as C
from generator import *

func_num = int(sys.argv[4])
parm_num = 6 # TODO: most have 6 regs in x64 mode, but here use 0-5.
var_num = int(sys.argv[1])
exp_num = int(sys.argv[2])
func_exp_num = int(sys.argv[3])
func_local_num = 10
cas_num = 4

def save_file(code):
    with open('test.c', 'w') as f:
        f.write(code)

def make_declare(var_index):
    return 'uint32_t var%s = %s' %(var_index, random_int32())

def make_func_call(func_lst):

    func_index = random_list_var(0, func_num)
    return 'var%s = func%d(%s)' % (random_list_var(0,var_num), func_index, ', '.join([('var%s' % (random_list_var(0,var_num))) for i in range(func_lst[func_index])]))

def make_exp(cas_num, v_num):
    _rnd = random_int32()
    if _rnd%cas_num == 0:
        return 'var%s = %svar%s' %(random_list_var(0,v_num), random_unary_op(), random_list_var(0,v_num))
    elif _rnd%cas_num == 1:
        return 'var%s = var%s %s var%s' % (random_list_var(0,v_num),random_list_var(0,v_num), random_judge_op(), random_list_var(0,v_num))
    elif _rnd%cas_num == 2:
        return 'var%s = var%s %s var%s ? var%s : var%s' % (random_list_var(0,v_num),random_list_var(0,v_num), random_judge_op(), random_list_var(0,v_num),random_list_var(0,v_num), random_list_var(0,v_num)) 
    elif _rnd%cas_num == 3:
        return 'var%s = var%s %s var%s' % (random_list_var(0,v_num), random_list_var(0,v_num), random_arith_op(), random_list_var(0,v_num))
'''
TODO: C.function('func', 'uint32_t',).add_arg(C.variable('var1', 'uint32_t'))
C.fcall('func%s'%(func_index), params=['v1','v2',])

'''
def make_func(func_name, para_num):
    _h = C.function(func_name, 'uint32_t',)
    for i in range(para_num):
        _h = _h.add_arg(C.variable('var%d'%i, 'uint32_t'))
    _w = C.sequence().append(_h)
    _f = C.block(indent=0)
    
    for i in range(para_num, func_local_num):
        _f.append(C.statement(make_declare(i)))

    for i in range(func_exp_num):
        _f.append(C.statement(make_exp(cas_num, func_local_num)))
    '''
    if para_num != 0:
        ret_var = random_list_var(0, func_local_num)
        _f.append(C.statement('return var%d'%(ret_var)))
    else:
        _f.append(C.statement('return 0'))
    '''
    ret_var = random_list_var(0, func_local_num)
    _f.append(C.statement('return var%d'%(ret_var)))

    _w = _w.append(_f)
    return _w

test = C.cfile('test.c')
test.code.append(C.sysinclude('stdio.h'))
test.code.append(C.sysinclude('stdlib.h'))
test.code.append(C.sysinclude('stdint.h'))
test.code.append(C.blank())

func_lst = []
for i in range(func_num):
    _parm_num = random_list_var(0, parm_num)
    test.code.append(make_func('func%d'%i, _parm_num))
    func_lst.append(_parm_num)

test.code.append(C.function('main', 'int',).add_arg(C.variable('argc', 'int')).add_arg(C.variable('argv', 'char', pointer=2)))

body = C.block(indent=0)
for cnt in range(var_num):
    body.append(C.statement(make_declare(cnt)))

for cnt in range(exp_num):
    body.append(C.statement(make_func_call(func_lst)))
    body.append(C.statement(make_exp(cas_num, var_num)))
#body.append(C.statement(C.fcall('printf').add_param(r'"Hello World!\n"')))
body.append(C.statement('return 0'))
test.code.append(body)

print(test.path)
save_file(str(test.code))

