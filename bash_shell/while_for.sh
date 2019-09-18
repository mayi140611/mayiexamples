#!/bin/bash

echo 'Input a number（press q to quit）'
# read num
num=5
while [ $num -gt 0 ];do
    echo $num
    num=`expr $num - 1`
done

for ((i=1;i<=5;i++))
do   
    echo $i
done