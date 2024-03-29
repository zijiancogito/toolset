#!/usr/bin/python3
import re
import os
import sys
import argparse
import binascii

import pdb
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

class AsmELFInfo:
  def __init__(self, filename):
    self.filename = filename
    self._rodata_tab = {}
    self._data_tab = {}
    self.get_data()
    self.get_rodata()

  @property
  def rodata(self):
    return self._rodata_tab

  @property
  def data(self):
    return self._data_tab

  def get_rodata(self):
    with open(self.filename, 'rb') as f:
      rodata_name = '.rodata'
      elffile = ELFFile(f)
      rodata = elffile.get_section_by_name(rodata_name)
      baseaddr = rodata.header['sh_offset']
      tmp_str = []
      addr = baseaddr
      for i in range(len(rodata.data())):
        tmp = rodata.data()[i]
        if tmp == 0x00:
          self._rodata_tab[str(hex(addr))] = ''.join([chr(x) for x in tmp_str])
          tmp_str = []
          addr = baseaddr + i
        else:
          tmp_str.append(tmp)
      # print(mem_map)
      # print(rodata.data())

  def get_data(self):
    with open(self.filename, 'rb') as f:
      rodata_name = '.data'
      elffile = ELFFile(f)
      rodata = elffile.get_section_by_name(rodata_name)
      baseaddr = rodata.header['sh_offset']
      tmp_str = []
      addr = baseaddr
      for i in range(len(rodata.data())):
        tmp = rodata.data()[i]
        if tmp == 0x00:
          self._data_tab[str(hex(addr))] = ''.join([chr(x) for x in tmp_str])
          tmp_str = []
          addr = baseaddr + i
        else:
          tmp_str.append(tmp)
    return

class CParser:
  STRING = ""


  def __init__(self, c_block):
    self._c_block = c_block
    self._c = c_block
    self._c_list = {}
    self._str_dict = {}
    
    # self.replace_string()
    # self.replace_char()

  def sub_table(self, table):
    lst = self._c_block.split(' ')
    for i in range(len(lst)):
      if lst[i] in table:
        lst[i] = table[lst[i]]
    return ' '.join(lst)


  def replace_string(self):
    parttern = '\"(.+?)\"'
    strs = re.findall(parttern, self._c_block)
    for string in strs:
      str_hex_list = _split_string(string)
      sub_str = ' '.join(str_hex_list)
      self._c = re.sub(string, sub_str, self._c,  1)
    
  def replace_char(self):
    parttern = "\'[\S\s]\'"
    chars = re.findall(parttern, self._c)
    for char in chars:
      self._c = re.sub(char, hex(int(char)), self._c)

  def _split_code(self):
    str_lst = self._c_block.split(' ')
    str_flag = 0
    
  def _split_string(self, string):
    tmp = []
    while len(string) == 0:
      tmp_str = ""
      if len(string) <=8:
        tmp_str = string[-1:]
        string = ""
      else:
        tmp_str = string[0:8]
        string = string[8:]
      tmp.append("0x%s"%binascii.b2a_hex(tmp_str.encode()).decode())
    return tmp
# class CNode:


# class CTree:
#   pass

class AsmParser:
  OFFSET_INS = "[\S\s]{0,}\[[a-z]{2,3}[\+\-]0x[0-9A-Fa-f]{1,16}\][\S\s]{0,}"
  IMM_INS = "[\S\s]{0,}[^+-]0x[0-9A-Fa-f]{0,16}\Z"
  ADDR_INS = "[\S\s]{0,}[^x0-9][0-9A-Fa-f]{0,16}\Z"

  IMME = "0x[0-9A-Fa-f]{0,16}\Z"
  ADDR = "[0-9A-Fa-f]{0,16}\Z"
  OFFSET = "[\S\s]{0,}[\+\-]0x[0-9A-Fa-f]{1,16}\]\Z"

  def __init__(self, asm_block):
    self._asm_block = asm_block.strip()# re.sub(" PTR", "", asm_block.strip())
    self._addr_tab = {}
    self._imm_tab = {}
    self._offset_tab = {}
    self._addr_map = {}
    self._imm_map = {}
    self._func_map = {}
    self._offset_map = {}
    self._insn_list = []
    self._set_insn_list()
    self._build_table(self._addr_tab, self.ADDR)
    self._build_table(self._imm_tab, self.IMME)
    self._build_table(self._offset_tab, self.OFFSET)

  @property
  def ins_seq(self):
    seq = []
    for ins_lst in self._insn_list:
      seq.append(ins_lst[0])
    return seq

  @property
  def func_map(self):
    return self._func_map
  
  @property
  def imm_map(self):
    return self._imm_map

  @property
  def offset_map(self):
    return self._offset_map

  @property
  def addr_map(self):
    return self._addr_map

  @property
  def insn_list(self):
    return self._insn_list

  @property
  def addr_tab(self):
    return self._addr_tab

  @property
  def imm_tab(self):
    return self._imm_tab

  @property
  def offset_tab(self):
    return self._offset_tab

  @property
  def new_asm(self):
    self.replace_all()
    asm = []
    for ins in self._insn_list:
      tmp = []
      for op in ins:
        op = ' '.join(op.split(' '))
        tmp.append(op)
      asm.append(' '.join(tmp))
    return '\t'.join(asm)

  def new_asm_list(self):
    self.replace_all()
    asm = []
    for ins in self._insn_list:
      tmp = []
      for op in ins:
        op = ' '.join(op.split(' '))
        tmp.append(op)
      asm.append(' '.join(tmp))
    return asm

  def _set_insn_list(self):
    for ins in self._asm_block.split(';'):
      ins = re.sub('[\s]{2,4}', '\t', ins)
      opc = [ins.split('\t')[0].strip()]
      if len(ins.split('\t')) > 1:
        ops = ins.split('\t')[1].split(',')
        for op in ops:
          opc.append(op.strip())
      self._insn_list.append(opc)

  def _build_table(self, tab, re_exp):
    for ins_index in range(len(self._insn_list)):
      ops = self._insn_list[ins_index]
      for op_index in range(len(ops[1:])):
        op = ops[op_index+1]
        if re.match(re_exp, op):
          if op in tab:
            tab[op].append((ins_index, op_index+1))
          else:
            tab[op] = [(ins_index, op_index+1)]

  def _replace_offset(self):
    count = 0
    for op in self._offset_tab:
      part = op.split(' ')[-1]
      tmp = re.sub('[\+\-]', ' ', part[1:-1]).split(' ')
      new_exp = "%s[%s]" % (tmp[0], "OFFSET"+str(count))
      self._offset_map[op.split(' ')[0]+ " "+tmp[0]+" "+tmp[1]] = "OFFSET"+str(count)
      for index in self._offset_tab[op]:
        self._insn_list[index[0]][index[1]] = ' '.join(op.split(' ')[:-1])+' '+new_exp
      count += 1

  def _replace_addr(self):
    count = 0
    func = 0
    for op in self._addr_tab:
      f = 0
      c = 0
      for index in self._addr_tab[op]:
        if self._insn_list[index[0]][0] == "call":
          self._insn_list[index[0]][index[1]] = "FUNC"+str(func)
          f = 1
        else:
          self._insn_list[index[0]][index[1]] = "ADDR"+str(count)
          c = 1
      self._func_map[op] = "FUNC"+str(func)
      self._addr_map[op] = "ADDR"+str(count)
      count += c
      func += f

  def _replace_imm(self):
    count = 0
    for op in self._imm_tab:
      self._imm_map[op] = "IMM"+str(count)
      for index in self._imm_tab[op]:
        self._insn_list[index[0]][index[1]] = "IMM"+str(count)
      count += 1

  def replace_all(self):
    self._replace_offset()
    self._replace_addr() 
    self._replace_imm()

def main():
  parser = argparse.ArgumentParser(description='re asm')
  parser.add_argument(dest='filenames',metavar='filename', nargs='*')
  parser.add_argument('-o', dest='outfile', action='store', required=True, help='output file')
  args = parser.parse_args()

  out = open(args.outfile, 'w')
  out_dic = {}
  for filename in args.filenames:
    with open(filename, 'r') as f:
      line = f.readline()
      while line:
        reasm = AsmParser(line.strip())
        out_dic[new_asm]
        out.write('\n')
        line = f.readline()
  out.close()

if __name__ == "__main__":
  a = AsmParser("je\t7e6;call\t530;call\t560;mov\tedx,DWORD PTR [rbp-0x30];mov\tDWORD PTR [rbp-0x2c],eax;add\trax,0x1;mov\tQWORD PTR [rbp-0x28],0x3")
  print(a.new_asm)
  print(a.addr_map)
  print(a.func_map)
  print(a.imm_map)
  print(a.offset_map)
  print(a.ins_seq)
  # e = AsmELFInfo("../../DataSets/ccode/a.out")
  # print(e.rodata)
  # print(e.data)
