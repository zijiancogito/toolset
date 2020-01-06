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
  def __init__(self, return_type, name, var_num, stmt_complex, param_list=[]):
    self.return_type = return_type
    self.func_name = name
    self.param_list = param_list
    self.local_var_num = var_num
    self.stmt_complex = stmt_complex

class FuncComplex:
  def __init__(self, 
               local_var_num, 
               art_stmt_cpx, 
               cmp_stmt_cpx,
               logic_stmt_cpx):
    self.local_var_num = local_var_num
    self.cmp_stmt_cpx = cmp_stmt_cpx
    self.art_stmt_cpx = art_stmt_cpx
    self.logic_stmt_cpx = logic_stmt_cpx

class ExpComplex:
  def __init__(self, var_num, imm_num):
    self.var_num = var_num
    self.imm_num = imm_num

class ConComplex:
  def __init__(self, exp_type, exp_complex):
    self.exp_type = exp_type
    self.exp_complex = exp_complex

class VarList:
  def __init__(self):
    self._types = []
    for i in UNSIGNED:
      for j in INT_TYPE:
        self._types.append("%s %s %s"%(i,j,'*'))
        self._types.append("%s %s`"%(i,j))
    for i in CHAR_TYPE:
      self._types.append(i)
      self._types.append("%s *"%(i))
    for i in REAL_TYPE:
      self._types.append(i)
      self._types.append("%s *"%(i))
    self.var_list = {}
    for i in self._types:
      self.var_list[i] = []

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

def random_imms(num):
  return [random.randint(a=-2**10, b=2**10) for i in range(num)]

def random_sub_list(oplist):
  op_len = random.randint(1, len(oplist)-1)
  return [random.choice(oplist) for i in range(op_len)]

def make_int_decl(var_index):
  signed = random.choice(UNSIGNED)
  tp = random.choice(INT_TYPE)
  var_type = "%s %s" % (signed, tp)
  var_name = "var%s" % (var_index)
  value = 0
  if signed == "unsigned":
    value = random_unsigned_int()
  else:
    value = random_signed_int()
  int_var = VarDecl(var_type, var_name, value)
  return int_var

def make_float_decl(var_index):
  var_type = random.choice(REAL_TYPE)
  var_name = "var%s" % (var_index)
  value = random_float()
  int_var = VarDecl(var_type, var_name, value)
  return int_var

def make_char_decl(var_index):
  var_type = random.choice(CHAR_TYPE)
  var_name = "var%s" % (var_index)
  value = random_char()
  char_var = VarDecl(var_type, var_name, value)
  return char_var

def make_array_int_decl():
  raise NotImplementedError

def make_array_real_decl():
  raise NotImplementedError

def make_array_str_decl(var_index, str_len):
  var_type = random.choice(CHAR_TYPE)
  var_name = "var%s" % (var_index)
  value = random_string()
  char_var = ArrayDecl(var_type, var_name, value, str_len)
  return char_var

def make_pointer_str_decl(var_index):
  var_type = "%s *" % (random.choice(CHAR_TYPE))
  var_name = "var%s" % (var_index)
  value = random_string()
  char_var = VarDecl(var_type, var_name, value)
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
  return param.strip()

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

def make_oplist(oplist, complex):
  return [random.choice(oplist) for i in range(complex)]

def make_func_decl(func_index, param_num, var_num, stmt_complex=0):
  param_list = [make_val_type() for index in range(param_num)]
  func_name = "func%s" % (func_index)
  ret_type = make_return_type()
  func = FuncDecl(ret_type, func_name, var_num, stmt_complex, param_list)
  return func

def make_func_call(funcs, vars):
  func = random.choice(funcs)
  name = func.func_name
  params = func.param_list
  p_l = []
  for p  in params:
    p_l.append(random.choice(vars.var_list[p]))
  return "%s(%s)" % (name, ", ".join(p_l))

def make_art_bin_exp(op1, op2):
  return "%s %s %s" % (op1,
                       random_arith_op(),
                       op2)

def make_logic_bin_exp(op1, op2):
  return "%s %s %s" % (op1,
                       random_logic_op(),
                       op2)

def make_cmp_bin_exp(op1, op2):
  return "%s %s %s" % (op1,
                       random_relate_op(),
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

def make_art_cmp_exp(oplist):
  tmp1 = tmp2 = oplist
  make_art_exp(random_sub_list(tmp1))
  make_art_exp(random_sub_list(tmp2))
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

def make_art_assignment_stmt(oplist, complex): # complex ExpComplex
  target = random.choice(oplist)
  tmp = oplist
  tmp.extend(random_imms(complex.imm_num))
  make_art_exp(tmp)
  return "%s = %s" % (target, tmp[0])
    
def make_con_stmt(oplist, complex):
  con = ""
  if complex == 1: # cmp_bin
    op1 = random.choice(oplist)
    op2 = random.choice(oplist)
    con = make_cmp_bin_exp(op1, op2)
  elif complex == 2: # logic_bin
    op1 = random.choice(oplist)
    op2 = random.choice(oplist)
    con = make_logic_bin_exp(op1, op2)
  elif complex == 3: # logic
    tmp = oplist
    make_logic_exp(tmp)
    con = tmp[0]
  elif complex == 4: # art_cmp
    con = make_art_cmp_exp(oplist)
  elif complex == 5: # logic_cmp
    con = make_logic_cmp_exp(tmp)
  elif complex == 6: # cmp_logic
    con = make_logic_cmp_exp(tmp)
  elif complex == 7: # mix_cmp
    con = make_mix_cmp_exp(oplist)
  else:
    con = make_mix_logic_exp(oplist, random.randint(1,5))
  return con

def make_if_stmt(oplist):
  body = "int i = 0;"
  return "if(%s){%s}else{%s}" % (make_con_stmt(oplist), body, body)
    
def make_while_stmt(oplist):
  body = "int i = 0;"
  return "while(%s){%s}" % (make_con_stmt(oplist), body)

def make_do_while_stmt(oplist):
  body = "int i = 0;"
  return "do{%s}while(%s)" % (body, make_con_stmt(oplist))

def is_pointer(t):
  if t.endswith('*'):
    return True
  else:
    return False

def make_func_body(func_decl, func_complex):
  param_lst = func_decl.param_list
  ret_type = func_decl.return_type
  func_name = func_decl.func_name
  _h = C.function(func_name, ret_type,)
  for i in range(len(param_lst)):
    _h = _h.add_arg(C.variable('param%d' % i, param_lst[i]))
  _w = C.sequence().append(_h)
  _f = C.block(indent=0)
  local_list = VarList()
  lvars = []
  # define var
  for i in range(func_complex.local_var_num):
    local_var_type = random.randint(0,4)
    var_decl = ""
    if local_var_type == 0: # int
      var = make_int_decl(i)
      local_list[var.var_type].append(var.var_name)
      if not is_pointer(var.var_type):
        local_list[var.var_type+" *"].append("&"+var.var_name)
      var_decl = "%s %s = %s" % (var.var_type, 
                                 var.var_name,
                                 var.value)
    elif local_var_type == 1: # real
      var = make_float_decl(i)
      local_list[var.var_type].append(var.var_name)
      if not is_pointer(var.var_type):
        local_list[var.var_type+" *"].append("&"+var.var_name)
      var_decl = "%s %s = %s" % (var.var_type, 
                                 var.var_name,
                                 var.value)
    elif local_var_type == 2: # char
      var = make_char_decl(i)
      local_list[var.var_type].append(var.var_name)
      if not is_pointer(var.var_type):
        local_list[var.var_type+" *"].append("&"+var.var_name)
      var_decl = "%s %s = \'%s\'" % (var.var_type, 
                                 var.var_name,
                                 var.value)
    elif local_var_type == 3: # char []
      var = make_array_str_decl(i, random.randint(2,10))
      local_list[var.var_type+" *"].append(var.var_name)
      var_decl = "%s %s[%d] = \"%s\"" % (var.var_type, 
                                         var.var_name, 
                                         var.shape,
                                         var.value) 
    elif local_var_type == 4: # char *
      var = make_pointer_str_decl(i)
      local_list[var.var_type].append(var.var_name)
      var_decl = "%s %s = \"%s\"" % (var.var_type, 
                                     var.var_name,
                                     var.value)
    else:
      raise IndexError
    _f.append(C.statement(var_decl))
    lvars.append(var)
  # art expression
  for i in range(func_complex.stmt_complex):
    pass

def make_func_body_easy(func_decl):
  param_lst = func_decl.param_list
  ret_type = func_decl.return_type
  func_name = func_decl.func_name
  _h = C.function(func_name, ret_type,)
  for i in range(len(param_lst)):
    _h = _h.add_arg(C.variable('param%d' % i, param_lst[i]))
  _w = C.sequence().append(_h)
  _f = C.block(indent=0)


if __name__ == '__main__':
  fm = FuncComplex(5,0)
  f = make_func_decl(0, 3)
  make_func_body(f, fm)
  ops = ["op1", "op2", "op1", "op3", "op5"]
  print(VarList().var_list)