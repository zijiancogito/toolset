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
LOGICAL_OPERATORS = ['&&', '||']
LOGICAL_SINGL_OPERATORS = ['!']
BIT_OPERATORS = ['&', '|', '^', '~', '<<', '>>']
SIZEOF = 'sizeof'
POINTER = ['*', '&']
MAX_PARAM_NUM = 6

FUNC_NUM = 100000


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
  def __init__(self, return_type, name, level,param_list=[]):
    self.return_type = return_type
    self.func_name = name
    self.param_list = param_list
    self.level = level

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
        self._types.append("%s %s"%(i,j))
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
  return random.randint(a=-2**14, b=2**15)

def random_unsigned_int():
  return random.randint(a=0, b=2**15)

def random_signed_short():
  return random.randint(a=-2**14, b=2**14)

def random_unsigned_short():
  return random.randint(a=0, b=2**15)

def random_float():
  return random.randint(a=-2**10, b=2**10) * 1.0 / random.randint(a=-2**31+1, b=2**31-1)

def random_char():
  ascii_code = random.randint(a=32, b=126)
  if ascii_code == 92:
    return '\\\\'
  elif ascii_code == 34:
    return '\\\"'
  elif ascii_code == 39:
    return '\\\''
  else:
    return chr(ascii_code)

def random_string(length):
  tmp_str = [random_char() for i in range(length-1)]
  return ''.join(tmp_str) + '\0'

def random_list_var(a, b):
  return random.randint(a, b-1)

def random_imms(num):
  return [random.randint(a=-2**10, b=2**10) for i in range(num)]

def random_sub_list(oplist):
  op_len = random.randint(1, len(oplist))
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

def make_int_decl_urand(var_index, tp):
  var_name = "var%s" % (var_index)
  value = 0
  if tp.startswith("unsigned"):
    value = random_unsigned_int()
  else:
    value = random_signed_int()
  int_var = VarDecl(tp, var_name, value)
  return int_var

def make_float_decl(var_index):
  var_type = random.choice(REAL_TYPE)
  var_name = "var%s" % (var_index)
  value = random_float()
  int_var = VarDecl(var_type, var_name, value)
  return int_var

def make_float_decl_urand(var_index, tp):
  var_name = "var%s" % (var_index)
  value = random_float()
  float_var = VarDecl(tp, var_name, value)
  return float_var

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
  value = random_string(str_len)
  char_var = ArrayDecl(var_type, var_name, value, str_len)
  return char_var

def make_pointer_str_decl(var_index):
  var_type = "%s *" % (random.choice(CHAR_TYPE))
  var_name = "var%s" % (var_index)
  value = random_string(random.randint(2,20))
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
  return ret.strip()

def make_oplist(oplist, complex):
  return [random.choice(oplist) for i in range(complex)]

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
  make_logic_exp(random_sub_list(tmp1))
  make_logic_exp(random_sub_list(tmp2))
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
  make_art_exp(random_sub_list(tmp1))
  make_logic_exp(random_sub_list(tmp2))
  return make_cmp_bin_exp(tmp1[0], tmp2[0])

def make_mix_logic_exp(oplist, complex):
  tmplist = []
  for i in range(complex):
    tmp = oplist
    ch = random.choice(['art', 'cmp', 'cmpart'])
    if ch == 'art':
      make_art_exp(random_sub_list(tmp))
      tmplist.append(tmp[0])
    elif ch == 'cmp':
      tmplist.append(make_cmp_bin_exp(random.choice(tmp), random.choice(tmp)))
    else:
      tmplist.append(make_art_cmp_exp(tmp))
  make_logic_exp(tmplist)
  return tmplist[0]

def make_art_assignment_stmt(oplist, complex): # complex ExpComplex
  target = random.choice(oplist)
  tmp = oplist
  tmp.extend(random_imms(complex))
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
    con = make_logic_cmp_exp(oplist)
  elif complex == 6: # cmp_logic
    con = make_logic_cmp_exp(oplist)
  elif complex == 7: # mix_cmp
    con = make_mix_cmp_exp(oplist)
  else:
    con = make_mix_logic_exp(oplist, random.randint(1,5))
  return con

def make_if_stmt(con):
  if_body = "int i = 0"
  else_body = "int i = 1"
  if_head = "if(%s)"%con
  else_head = "else"
  if_block = C.block(indent=2, innerIndent=2, head=if_head)
  if_block.append(C.statement(if_body))
  else_block = C.block(indent=2, innerIndent=2, head=else_head)
  else_block.append(C.statement(else_body))
  return if_block, else_block
    
def make_while_stmt(con):
  body = "int i = 2"
  head = "while(%s)"%con
  block = C.block(indent=2, innerIndent=2, head=head)
  block.append(C.statement(body))
  return block

def make_do_while_stmt(con):
  body = "int i = 3"
  tail = "while(%s);"%con
  block = C.block(indent=2, innerIndent=2, head="do", tail=tail)
  block.append(C.statement(body))
  return block

def is_pointer(t):
  if t.endswith('*'):
    return True
  else:
    return False

def make_func_decl(func_index, param_num, level):
  param_list = [make_val_type() for index in range(param_num)]
  func_name = "func%s" % (func_index)
  ret_type = make_return_type()
  func = FuncDecl(ret_type, func_name, level, param_list)
  return func

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
      local_list.var_list[var.var_type].append(var.var_name)
      if not is_pointer(var.var_type):
        local_list.var_list[var.var_type+" *"].append("&"+var.var_name)
      var_decl = "%s %s = %s" % (var.var_type, 
                                 var.var_name,
                                 var.value)
    elif local_var_type == 1: # real
      var = make_float_decl(i)
      local_list.var_list[var.var_type].append(var.var_name)
      if not is_pointer(var.var_type):
        local_list.var_list[var.var_type+" *"].append("&"+var.var_name)
      var_decl = "%s %s = %s" % (var.var_type, 
                                 var.var_name,
                                 var.value)
    elif local_var_type == 2: # char
      var = make_char_decl(i)
      local_list.var_list[var.var_type].append(var.var_name)
      if not is_pointer(var.var_type):
        local_list.var_list[var.var_type+" *"].append("&"+var.var_name)
      var_decl = "%s %s = \'%s\'" % (var.var_type, 
                                 var.var_name,
                                 var.value)
    elif local_var_type == 3: # char []
      var = make_array_str_decl(i, random.randint(2,10))
      local_list.var_list[var.var_type+" *"].append(var.var_name)
      var_decl = "%s %s[%d] = \"%s\"" % (var.var_type, 
                                         var.var_name, 
                                         var.shape,
                                         var.value) 
    elif local_var_type == 4: # char *
      var = make_pointer_str_decl(i)
      local_list.var_list[var.var_type].append(var.var_name)
      var_decl = "%s %s = \"%s\"" % (var.var_type, 
                                     var.var_name,
                                     var.value)
    else:
      raise IndexError
    _f.append(C.statement(var_decl))
    lvars.append(var)
 

def make_func_call(funcs, vars):
  func = random.choice(funcs)
  name = func.func_name
  params = func.param_list
  ret = func.return_type
  p_l = []
  for p  in params:
    p_l.append(random.choice(vars.var_list[p]))
  return "%s(%s)" % (name, ", ".join(p_l)), ret

def make_return_value(oplist, complex):
  tmp = [random.choice(oplist) for i in range(complex)]
  ch = random.randint(0,8)
  ret = ""
  if ch == 0: # art
    make_art_exp(tmp)
    ret = tmp[0]
  else:
    mode = random.randint(1,8)
    ret = make_con_stmt(tmp, mode)
  return ret


def call_art_assignment_stmt(call_list, var_list, complex): # complex ExpComplex
  target = random.choice(var_list)
  tmp = call_list+var_list
  tmp.extend(random_imms(complex))
  make_art_exp(tmp)
  return "%s = %s" % (target, tmp[0])

def sub_list(level, oplist):
  op_len = random.randint(level, len(oplist))
  return [random.choice(oplist) for i in range(op_len)]

def make_func_body_easy(func_decl, level, funcs): # level(1,5)
  local_list = VarList()
  param_lst = func_decl.param_list
  ret_type = func_decl.return_type
  func_name = func_decl.func_name

  _h = C.function(func_name, ret_type,)
  for i in range(len(param_lst)):
    if ('*' or '[') not in param_lst[i]:
      local_list.var_list[param_lst[i]].append('param%d'%i)
      local_list.var_list[param_lst[i]+" *"].append('&param%d'%i)
    else:
      local_list.var_list[param_lst[i]].append('param%d'%i)
    _h = _h.add_arg(C.variable('param%d' % i, param_lst[i]))
  _w = C.sequence().append(_h)
  _f = C.block(indent=2)

  local_var_index = 0
  var_decls = []
  var_decls.append("int i")
  stmt_decls = []
  block_decls = []
  int_type = []
  
  for tp in INT_TYPE:
    int_type.append("%s %s" % ("unsigned", tp))
    int_type.append("%s %s" % ("signed", tp))

  # define int
  for tp in int_type:
    ints = []
    for i in range(level):
      var = make_int_decl_urand(local_var_index, tp)
      var_decl = "%s %s = %s"%(tp,var.var_name, var.value)
      var_decls.append(var_decl)
      ints.append(var.var_name)
      local_var_index += 1
      local_list.var_list[tp].append(var.var_name)
      local_list.var_list[tp+" *"].append('&'+var.var_name)
    for i in range(len(param_lst)):
      if param_lst[i] == tp:
        ints.append("param%d"%(i))
    for i in range(level):
      tmp = sub_list(level, ints)
      art_stmt = make_art_assignment_stmt(tmp, level)
      stmt_decls.append(art_stmt)

  # define float
  for tp in REAL_TYPE:
    floats = []
    for i in range(level):
      var = make_float_decl_urand(local_var_index, tp)
      var_decl = "%s %s = %s"%(tp, var.var_name, var.value)
      var_decls.append(var_decl)
      floats.append(var.var_name)
      local_var_index += 1
      local_list.var_list[tp].append(var.var_name)
      local_list.var_list[tp+" *"].append('&'+var.var_name)
    for i in range(len(param_lst)):
      if param_lst[i] == tp:
        ints.append("param%d"%(i))
    for i in range(level):
      tmp = sub_list(level, ints)
      art_stmt = make_art_assignment_stmt(tmp, level)
      stmt_decls.append(art_stmt)

  # define char
  for tp in CHAR_TYPE:
    chars = []
    for i in range(level):
      var = make_char_decl(local_var_index)
      var_decl = "%s %s = \'%s\'"%(tp, var.var_name, var.value)
      var_decls.append(var_decl)
      chars.append(var.var_name)
      local_var_index += 1
      local_list.var_list[tp].append(var.var_name)
      local_list.var_list[tp+" *"].append('&'+var.var_name)

  # define char *
  charps = []
  for i in range(level):
    var = make_pointer_str_decl(local_var_index)
    var_decl = "char * %s = \"%s\""%(var.var_name, var.value)
    var_decls.append(var_decl)
    charps.append(var.var_name)
    local_var_index += 1
  local_list.var_list["char *"].append(var.var_name)
  
  # define char []
  charas = []
  for i in range(level):
    cspace = random.randint(2,20)
    clen = random.randint(2,cspace)
    var = make_array_str_decl(local_var_index, clen)
    var_decl = "char %s[%s] = \"%s\""%(var.var_name, cspace, var.value)
    var_decls.append(var_decl)
    charas.append(var.var_name)
    local_var_index += 1
  local_list.var_list["char *"].append(var.var_name)

  # define func_call
  calls = {}
  for i in range(level):
    call_body, ret = make_func_call(funcs, local_list)
    call_decl = ""
    if ret == 'void':
      call_decl = call_body
    else:
      call_decl = "%s ret%s = %s" % (ret, i, call_body)
      if ret in calls:
        calls[ret].append(call_body)
      else:
        calls[ret] = [call_body]
    stmt_decls.append(call_decl)
  
  # define func call art
  call_num = random.randint(1, level)
  var_num = random.randint(1, level)
  for tp in calls:
    if ("signed" in tp) and ("*" not in tp):
      tmp1 = [random.choice(calls[tp]) for i in range(call_num)]
      tmp2 = [random.choice(local_list.var_list[tp]) for i in range(var_num)]
      art_decl = call_art_assignment_stmt(tmp1, tmp2, level)
      stmt_decls.append(art_decl)
  
  # define con
  call_num = random.randint(0, level)
  var_num = random.randint(2, level)
  for tp in calls:
    tmp1 = [random.choice(calls[tp]) for i in range(call_num)]
    tmp2 = [random.choice(local_list.var_list[tp]) for i in range(var_num)]
    tmp3 = [random_signed_int() for i in range(level)]
    tmp4 = ["\'%s\'"%random_char() for i in range(level)]
    tmp = tmp1 + tmp2 + tmp3 + tmp4
    for i in range(1,9):
      con_decl = "i = %s"%(make_con_stmt(tmp, i))
      stmt_decls.append(con_decl)

  # define if
  call_num = random.randint(0, level)
  var_num = random.randint(2, level)
  for tp in calls:
    tmp1 = [random.choice(calls[tp]) for i in range(call_num)]
    tmp2 = [random.choice(local_list.var_list[tp]) for i in range(var_num)]
    tmp3 = [random_signed_int() for i in range(level)]
    tmp4 = ["\'%s\'"%random_char() for i in range(level)]
    tmp = tmp1 + tmp2 + tmp3 + tmp4
    for i in range(1,9):
      con_decl = make_con_stmt(tmp, i)
      if_decl, else_decl = make_if_stmt(con_decl)
      block_decls.append(if_decl)
      block_decls.append(else_decl)

  # define while
  call_num = random.randint(0, level)
  var_num = random.randint(2, level)
  for tp in calls:
    tmp1 = [random.choice(calls[tp]) for i in range(call_num)]
    tmp2 = [random.choice(local_list.var_list[tp]) for i in range(var_num)]
    tmp3 = [random_signed_int() for i in range(level)]
    tmp4 = ["\'%s\'"%random_char() for i in range(level)]
    tmp = tmp1 + tmp2 + tmp3 + tmp4
    for i in range(1,9):
      con_decl = make_con_stmt(tmp, i)
      while_decl = make_while_stmt(con_decl)
      block_decls.append(while_decl)

  # define do while
  call_num = random.randint(0, level)
  var_num = random.randint(2, level)
  for tp in calls:
    tmp1 = [random.choice(calls[tp]) for i in range(call_num)]
    tmp2 = [random.choice(local_list.var_list[tp]) for i in range(var_num)]
    tmp3 = [random_signed_int() for i in range(level)]
    tmp4 = ["\'%s\'"%random_char() for i in range(level)]
    tmp = tmp1 + tmp2 + tmp3 + tmp4
    for i in range(1,9):
      con_decl = make_con_stmt(tmp, i)
      do_decl = make_do_while_stmt(con_decl)
      block_decls.append(do_decl)

  for decl in var_decls:
    _f.append(C.statement(decl))
  
  for decl in stmt_decls:
    _f.append(C.statement(decl))

  for decl in block_decls:
    _f.append(decl)
  
  if ret_type != 'void':
    call_num = random.randint(0, level)
    var_num = random.randint(2, level)
    tmp1 = []
    if ret_type in calls:
      tmp1 = [random.choice(calls[ret_type]) for i in range(call_num)]
    tmp2 = [random.choice(local_list.var_list[ret_type]) for i in range(var_num)]
    tmp3 = [random_signed_int() for i in range(level)]
    tmp4 = ["\'%s\'"%random_char() for i in range(level)]
    tmp = tmp1 + tmp2 + tmp3 + tmp4
    ret_value = make_return_value(tmp, level)
    ret_decl = "return %s" % ret_value
    _f.append(C.statement(ret_decl))
  _w = _w.append(_f)
  return _w


def make_decls(levelrange, num):
  func_decls = []
  index = 0
  for level in range(1, levelrange+1):
    for i in range(num):
      pnum = random.randint(0,5)
      decl = make_func_decl(index, pnum, level)
      func_decls.append(decl)
      index += 1
  return func_decls

def generator(level, num):
  func_decl_list = make_decls(level, num)
  test = C.cfile('test.c')
  test.code.append(C.blank())
  for func in func_decl_list:
    decl = "%s %s(%s)"%(func.return_type, 
                        func.func_name,
                        ", ".join(func.param_list))
    test.code.append(C.statement(decl))
  for func in func_decl_list:
    test.code.append(make_func_body_easy(func, level, func_decl_list))
  test.code.append(C.function('main', 'int',).add_arg(C.variable('argc', 'int')).add_arg(C.variable('argv', 'char', pointer=2)))
  body = C.block(indent=0)
  body.append(C.statement('return 0'))
  test.code.append(body)
  print(test.path)
  save_file(str(test.code))

if __name__ == '__main__':
  generator(3,10)