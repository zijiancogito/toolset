#!/usr/bin/python3
import os, sys
import cfile as C
import random

UNSIGNED = ['unsigned', 'signed']
INT_TYPE = ['short', 'int', 'long', 'long long']
CHAR_TYPE = ['char']
REAL_TYPE = ['float', 'double']
VOID_TYPE = ['void']

ARITHMETIC_OPERATORS = ['+', '-', '*', '/', '%']
COMPARE_OPERATORS = ['==', '!=', '>', '<', '>=', '<=']
LOGICAL_OPERATORS = ['&&', '||', '!']
BIT_OPERATORS = ['&', '|', '^', '~', '<<', '>>']
SIZEOF = 'sizeof'
POINTER = ['*', '&']
MAX_PARAM_NUM = 6

class VarDecl:
  def __init__(self, var_type, name, value = None):
    self.var_type = var_type
    self.var_name = name
    self.value = value

class ArrayDecl:
  def __init__(self, var_type, name, shape = 0, value = None):
    self.var_type = var_type
    self.var_name = name
    self.value = value
    self.shape = shape

class FuncDecl:
  def __init__(self, return_type, name, param_list=[]):
    self.return_type = return_type
    self.func_name = name
    self.param_list = param_list

class FuncComplex:
  def __init__(self, local_var_num, stmt_complex):
    self.local_var_num = local_var_num
    self.stmt_complex = stmt_complex

def save_file(code):
  with open('test.c', 'w') as f:
    f.write(code)

def random_arith_op():
  return random.choice(ARITHMETIC_OPERATORS)

def random_relate_op():
  return random.choice(COMPARE_OPERATORS)

def random_logic_op():
  return random.choice(LOGICAL_OPERATORS)

def random_bit_op():
  return random.choice(BIT_OPERATORS)

def random_signed_int():
  return random.randint(a=-2**10, b=2**10)

def random_unsigned_int():
  return random.randint(a=0, b=2**10)

def random_float():
  return random.randint(a=-2**10, b=2**10) * 1.0 / random.randint(a=-2**31+1, b=2**31-1)

def random_char():
  return chr(random.randint(a=32, b=126))

def random_string(length):
  tmp_str = [random_char() for i in range(0,length)]
  return ''.join(tmp_str)

def random_list_var(a, b):
  return random.randint(a, b-1)

def make_int_decl(var_index):
  var_type = "%s %s" % (random.choice(UNSIGNED), random.choice(INT_TYPE))
  var_name = "var%s" % (var_index)
  int_var = VarDecl(var_type, var_name)
  return int_var

def make_float_decl(var_index):
  var_type = random.choice(REAL_TYPE)
  var_name = "var%s" % (var_index)
  int_var = VarDecl(var_type, var_name)
  return int_var

def make_char_decl(var_index):
  var_type = random.choice(CHAR_TYPE)
  var_name = "var%s" % (var_index)
  char_var = VarDecl(var_type, var_name)
  return char_var

def make_array_int_decl():
  raise NotImplementedError

def make_array_real_decl():
  raise NotImplementedError

def make_array_str_decl(var_index, str_len):
  var_type = random.choice(CHAR_TYPE)
  var_name = "var%s" % (var_index)
  char_var = ArrayDecl(var_type, var_name, str_len)
  return char_var

def make_pointer_str_decl(var_index):
  var_type = "%s *" % (random.choice(CHAR_TYPE))
  var_name = "var%s" % (var_index)
  char_var = VarDecl(var_type, var_name)
  return char_var

def make_val_type():
  tp = random.randint(a=0, b=2)
  param = ""
  if tp == 0: #int
    param = "%s %s %s" % (random.choice(UNSIGNED),
                                  random.choice(INT_TYPE),
                                  random.choice(['*', '']))
  elif tp == 1: #char
    param = "%s %s" % (random.choice(CHAR_TYPE),
                               random.choice(['*', '']))
  else: #real
    param = "%s %s" % (random.choice(REAL_TYPE),
                               random.choice(['*', '']))
  return param

def make_return_type():
  tp = random.randint(a=0, b=3)
  ret = ""
  if tp == 0: #int
    ret = "%s %s %s" % (random.choice(UNSIGNED),
                        random.choice(INT_TYPE),
                        random.choice(['*', '']))
  elif tp == 1: #char
    ret = "%s %s" % (random.choice(CHAR_TYPE),
                     random.choice(['*', '']))
  elif tp == 2: #real
    ret = "%s %s" % (random.choice(REAL_TYPE),
                     random.choice(['*', '']))
  else:
    ret = 'void'
  return ret

def make_func_decl(func_index, param_num):
  param_list = [make_val_type() for index in range(param_num)]
  func_name = "func%s" % (func_index)
  ret_type = make_return_type()
  func = FuncDecl(ret_type, func_name, param_list)
  return func

def make_func_call(func_lst, param_num, func_num):
  func_index = random_list_var(0, func_num)
  return "func%d(%s)" 

def make_art_bin_exp(op1, op2):
  return "%s %s %s" % (op1,
                       random.choice(ARITHMETIC_OPERATORS),
                       op2)

def make_logic_bin_exp(op1, op2):
  return "%s %s %s" % (op1,
                       random.choice(LOGICAL_OPERATORS),
                       op2)

def make_cmp_bin_exp(op1, op2):
  return "%s %s %s" % (op1,
                       random.choice(COMPARE_OPERATORS),
                       op2)

def make_art_exp(oplist):
  if len(oplist) == 1:
    pass
  elif len(oplist) == 2:
    new_op = make_art_bin_exp(oplist[0], oplist[1])
    oplist.pop(0)
    oplist.pop(0)
    oplist.append(new_op)
  else:
    op1_index = random.randint(0, len(oplist) - 1)
    op2_index = random.randint(0, len(oplist) - 1)
    op1 = oplist[op1_index]
    op2 = oplist[op2_index]
    if op1_index < op2_index:
      oplist.pop(op1_index)
      oplist.pop(op2_index - 1)
    elif op1_index > op2_index:
      oplist.pop(op2_index)
      oplist.pop(op1_index - 1)
    else:
      oplist.pop(op1_index)
    new_op = make_art_bin_exp(op1, op2)
    oplist.append("(%s)"%new_op)
    make_art_exp(oplist)

def make_logic_exp(oplist):
  if len(oplist) == 1:
    pass
  elif len(oplist) == 2:
    new_op = make_logic_bin_exp(oplist[0], oplist[1])
    oplist.pop(0)
    oplist.pop(0)
    oplist.append(new_op)
  else:
    op1_index = random.randint(0, len(oplist) - 1)
    op2_index = random.randint(0, len(oplist) - 1)
    op1 = oplist[op1_index]
    op2 = oplist[op2_index]
    if op1_index < op2_index:
      oplist.pop(op1_index)
      oplist.pop(op2_index - 1)
    elif op1_index > op2_index:
      oplist.pop(op2_index)
      oplist.pop(op1_index - 1)
    else:
      oplist.pop(op1_index)
    new_op = make_logic_bin_exp(op1, op2)
    oplist.append("(%s)"%new_op)
    make_logic_exp(oplist)

def random_sub_list(oplist, complex):
  op_len = random.randint(1, complex)
  return [random.choice(oplist) for i in range(op_len)]

def make_art_cmp_exp(oplist, complex):
  tmp1 = tmp2 = oplist
  make_art_exp(random_sub_list(tmp1, complex))
  make_art_exp(random_sub_list(tmp2, complex))
  return make_cmp_bin_exp(tmp1[0], tmp2[0])

def make_logic_cmp_exp(oplist):
  tmp1 = tmp2 = oplist
  make_logic_exp(random_sub_list(tmp1, complex))
  make_logic_exp(random_sub_list(tmp2, complex))
  return make_cmp_bin_exp(tmp1[0], tmp2[0])

def make_cmp_logic_exp(oplist, complex):
  tmplist=[]
  for i in range(complex):
    op1 = random.choice(oplist)
    op2 = random.choice(oplist)
    tmplist.append(make_cmp_bin_exp(op1, op2))
  make_logic_exp(tmplist)
  return tmplist[0]

def make_mix_cmp_exp(oplist):
  tmp1 = tmp2 = oplist
  make_art_exp(random_sub_list(tmp1, complex))
  make_logic_exp(random_sub_list(tmp2, complex))
  return make_cmp_bin_exp(tmp1[0], tmp2[0])

def make_mix_logic_exp(oplist, complex):
  tmplist = []
  for i in range(complex):
    tmp = oplist
    ch = random.choice(['art', 'cmp', 'cmpart'])
    if ch == 'art':
      make_art_exp(random_sub_list(tmp, complex))
      tmplist.append(tmp[0])
    elif ch == 'cmp':
      tmplist.append(make_cmp_bin_exp(random.choice(tmp), random.choice(tmp)))
    else:
      tmplist.append(make_art_cmp_exp(tmp, complex))
  make_logic_exp(tmplist)
  return tmplist[0]

def make_

def make_oplist(oplist, complex):
  return [random.choice(oplist) for i in range(complex)]

def make_func_body(func_decl, func_complex):
  param_lst = func_decl.param_list
  ret_type = func_decl.return_type
  func_name = func_decl.func_name
  _h = C.function(func_name, ret_type,)
  for i in range(len(param_lst)):
    _h = _h.add_arg(C.variable('param%d' % i, param_lst[i]))
  _w = C.sequence().append(_h)
  _f = C.block(indent=0)
  local_list = []
  # declare var
  for i in range(func_complex.local_var_num):
    local_var_type = random.randint(0,4)
    var_decl = ""
    if local_var_type == 0: # int
      var = make_int_decl(i)
      var_decl = "%s %s" % (var.var_type, var.var_name)
    elif local_var_type == 1: # real
      var = make_float_decl(i)
      var_decl = "%s %s" % (var.var_type, var.var_name)
    elif local_var_type == 2: # char
      var = make_char_decl(i)
      var_decl = "%s %s" % (var.var_type, var.var_name)
    elif local_var_type == 3: # char []
      var = make_array_str_decl(i, random.randint(2,10))
      var_decl = "%s %s[%d]" % (var.var_type, var.var_name, var.shape) 
    elif local_var_type == 4: # char *
      var = make_pointer_str_decl(i)
      var_decl = "%s %s" % (var.var_type, var.var_name) 
    else:
      raise IndexError
    _f.append(C.statement(var_decl))
    local_list.append(var)
  # init var
  #for var in local_list:
    

if __name__ == '__main__':
  fm = FuncComplex(5,0)
  f = make_func_decl(0, 3)
  make_func_body(f, fm)
  ops = ["op1", "op2", "op1", "op3", "op5"]
  make_exp(ops)
  print(ops)