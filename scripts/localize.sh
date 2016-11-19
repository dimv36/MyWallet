#!/bin/bash

echo "Localizing application..."
LUPDATE=`which pylupdate5`

if [ "x$LUPDATE" == "x" ]
then
    echo "Needed PyQt5 dev tools package..."
    exit 1
fi

$LUPDATE -translate-function tr ../pymywallet.pro
