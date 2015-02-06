#!/bin/sh
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

/bin/sh $SCRIPTPATH/python_27/run.sh $1 $2
