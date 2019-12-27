#!/bin/bash

cpath="/home/jho/Leetcode/workspace/purecode/"
spath="/home/jho/Leetcode/workspace/asm/"
filelist=`ls ${cpath}`
for file in $filelist
do
    g++ -std=c++11 -Wa,-adhln -g ${cpath}${file} > ${spath}${file%.cpp}".s"
done
