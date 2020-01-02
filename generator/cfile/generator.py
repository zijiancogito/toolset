import random

arith_op = ['+', '-', '*', '/', '%', '^', '&', '|', '<<', '>>']

'''
not considered: ++ -- sizeof
'''
unary_op = ['+', '-', '~', '!']
judge_op = ['==', '!=', '>', '<', '>=', '<=', '&&', '||']

def random_int32():
    return random.randint(a=0, b=2**32-1)

'''
simple expression format: 
1. var1 = unary_op var2
2. var1 = var2 arith_op var3
'''

def random_unary_op():
    return random.choice(unary_op) # unary_op[random_int() % len(unary_op)]
def random_arith_op():
    return random.choice(arith_op) # arith_op[random_int() % len(arith_op)]
def random_judge_op():
    return random.choice(judge_op)
def ri(_l):
    return random.choice(_l)
def random_alph_var():
    return chr(ord('a')+random.randint(a=0,b=2**32)%26)

def random_list_var(a, b):
    return random.randint(a,b-1) # a <= x < b