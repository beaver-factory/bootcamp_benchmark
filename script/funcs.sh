#!/bin/bash

directory=$1

cp ../an_example_function/app.py $directory
cp -r ../an_example_function/__tests__ $directory/__tests__
rm $directory/readme.md