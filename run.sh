#!/bin/bash
# gen_yaml
# python3 gen_yaml.py [source_code_dir] [yaml_dir]
python3 rename/gen_yaml.py ../DataSets/ccode/ ../DataSets/yaml/
echo "yaml finished!\n"
cp ../DataSets/ccode/* ../DataSets/src/
echo "copy code to src\n"
# rename
# python3 rename.py [yaml_file_dir] [code_file_dir]
python3 rename/rename.py ../DataSets/yaml/ ../DataSets/src/
echo "rename code\n"
# compile new source code
../DataSets/src/make
echo "compile\n"
mv ../DataSets/src/*.c ../DataSets/src_1/code/
echo "move code\n"
mv ../DataSets/src/* ../DataSets/src_1/bin/
rm ../DataSets/src_1/bin/Makefile
echo "move bin"
# DASM line
# python3 dasm.py [binary files dir] [asm files dir]
python3 dasm.py ../DataSets/src_1/bin/ ../DataSets/src_1/asm_line/
echo "disassemble\n"
# code2line
# python3 code2line.py [source code dir] [out code dir]
python3 code2line.py ../DataSets/src_1/code/ ../DataSets/src_1/code2line/
echo "code to line\n"
# Code parser
# python3 parserFile.py [source dir] [parser dir]
python3 parserFile.py ../DataSets/src_1/code2line/ ../DataSets/src_1/parsercode/
# CvsAsm
# python3 CvsAsm.py [code_line_dir] [asm_line_dir] [out file]
python3 CvsAsm.py ../DataSets/src_1/parsercode/ ../DataSets/src_1/asm_line/ ../DataSets/src_1/data
echo "finished\n"

#3670