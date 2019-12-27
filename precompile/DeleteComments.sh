#!/bin/bash

workspace="/home/jho/Leetcode/workspace/"
sourcecodepath="${workspace}cpp_sourcecode/"
outfilepath="${workspace}procomments/"
filelist=`ls $sourcecodepath`
for file in $filelist
do
    g++ -std=c++11 -E -fpreprocessed ${sourcecodepath}${file} -o ${outfilepath}${file}
done
