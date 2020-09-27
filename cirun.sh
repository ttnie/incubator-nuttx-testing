#!/usr/bin/env bash

set -e
set -o xtrace

WD=$(cd $(dirname $0) && pwd)
WORKSPACE=$(cd $WD/.. && pwd -P)
nuttx=$WORKSPACE/nuttx
logs=${WD}/logs

image=`find ${nuttx} -type f -name 'nuttx'`
path=${image%/*/*}
python3 ${WD}/testrun/run.py -l ${logs} -p ${path}
#python3 ${WD}/testrun/genReport.py -l ${logs}
