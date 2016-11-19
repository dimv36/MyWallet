#!/bin/bash

uic=$(which pyuic5)

for file in *.ui; do
  echo "compiling ${file}"
  ${uic} "${file}" > ui_${file%%.*}.py
done
