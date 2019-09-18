#!/bin/bash

echo 'Please press a number to select options'
# read num
num=$1
case $num in
    1)  echo 'option 1'
    ;;
    2)  echo 'option 2'
    ;;
    3)  echo 'option 3'
    ;;
    *)   echo 'Other'
    ;;
esac
