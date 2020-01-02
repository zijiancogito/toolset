#!/bin/sh

#for i in {1..$1}
for i in `seq 1 $1`
do 
	echo $i
	python3 $2 10 10 10 10
	./build.sh
	mv test.lst batch_data/test$i.lst
done
