import cfile as C
from generator import *

def save_file(code):
    with open('test.c', 'w') as f:
        f.write(code)

test = C.cfile('test.c')
test.code.append(C.sysinclude('stdio.h'))
test.code.append(C.sysinclude('stdlib.h'))
test.code.append(C.sysinclude('stdint.h'))
test.code.append(C.blank())
test.code.append(C.function('main', 'int',).add_arg(C.variable('argc', 'int')).add_arg(C.variable('argv', 'char', pointer=2)))

var_num = 10
body = C.block(indent=4)
for cnt in range(var_num):
    body.append(C.statement('uint32_t var%s = %s' %(str(cnt), random_int32())))
exp_num = 20
for cnt in range(exp_num):
    if cnt%2 == 0:
        body.append(C.line('if (var%s %s var%s)' % (random_list_var(0,var_num), random_judge_op(), random_list_var(0,var_num)))) # if
        if_body = C.block(indent=8)

        if_body.append(C.statement('var%s = %svar%s' %(random_list_var(0,var_num), random_unary_op(), random_list_var(0,var_num))))
        body.append(if_body)
    else:
        body.append(C.line('else')) # else
        else_body = C.block(indent=8)
        

        else_body.append(C.statement('var%s = var%s %s var%s' %(random_list_var(0,var_num), random_list_var(0,var_num), random_arith_op(), random_list_var(0,var_num))))
        
        body.append(else_body)
#body.append(C.statement(C.fcall('printf').add_param(r'"Hello World!\n"')))
body.append(C.statement('return 0'))
test.code.append(body)

print(test.path)
print(test.code)
save_file(str(test.code))