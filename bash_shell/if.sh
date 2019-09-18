#!/bin/bash

pip install numpy

if [ $? = 0 ]; then
echo "Installation Successfully"
else
echo "Problems to install Essential packages, check this!"
exit 1
fi