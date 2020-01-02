import sys
import cfile as C
from generator import *

def save_file(code):
    with open('test.c', 'w') as f:
        f.write(code)

def random_var():
    global arr_lst, ptr_lst, nor_lst
    _rnd = random_int32()
    if _rnd%3 == 0:
        return 'var%s' % ri(nor_lst)
    elif _rnd%3 == 1:
        _arr_var = ri(arr_lst)
        return 'var%s[%s]' % (_arr_var[0], random_list_var(0,_arr_var[1]))
    else:
        return '*var%s' % ri(ptr_lst)

test = C.cfile('test.c')
test.code.append(C.sysinclude('stdio.h'))
test.code.append(C.sysinclude('stdlib.h'))
test.code.append(C.sysinclude('stdint.h'))
test.code.append(C.blank())
test.code.append(C.function('main', 'int',).add_arg(C.variable('argc', 'int')).add_arg(C.variable('argv', 'char', pointer=2)))

var_num = int(sys.argv[1])
body = C.block(indent=0)

'''
v include: var arr_var ptr_var 
v = v op v
ori_var: (&| )foo
arr_var: foo[rnd]
ptr_var: (*|&| )foo
mix_var
'''

var_cas_num = 3

ptr_num = 1
arr_lst = []
ptr_lst = []
nor_lst = []
for cnt in range(var_num):
    _arr_num = (random_int32()%10) + 2
    _rnd = random_int32()
    if _rnd%3 == 0:
        _stat = ("%s = %s") %(C.variable("var%s"%str(cnt)), random_int32())
        nor_lst.append(cnt)
    elif _rnd%3 == 1:
        _stat = ("%s = {%s}") %(C.variable("var%s"%str(cnt), array=_arr_num), random_int32())
        arr_lst.append((cnt, _arr_num))
    else:
        _stat = ("%s = %s") %(C.variable("var%s"%str(cnt), pointer=ptr_num), random_int32())
        ptr_lst.append(cnt)
    #print (_stat)
    body.append(C.statement(_stat))
    #body.append(C.statement('uint32_t var%s = %s' %(str(cnt), random_int32()))) 

exp_num = int(sys.argv[2])
cas_num = 3
for cnt in range(exp_num):
    _rnd = random_int32()
    if _rnd%cas_num == 0:
        body.append(C.statement('%s = %s %s' %(random_var(), random_unary_op(), random_var())))
    elif _rnd%cas_num == 1:
        body.append(C.statement('%s = %s %s %s' % (random_var(), random_var(), random_arith_op(), random_var())))  
    elif _rnd%cas_num == 2:
        body.append(C.statement('%s = &%s' % (random_var(), random_var())))

#body.append(C.statement(C.fcall('printf').add_param(r'"Hello World!\n"')))
body.append(C.statement('return 0'))
test.code.append(body)

print(test.path)
print(str(test.code))
save_file(str(test.code))

