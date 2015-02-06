#!/bin/sh
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

python2 $SCRIPTPATH/main.py $1 $2
