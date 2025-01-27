#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Optimizing Heaters"
python3 ${PYTHONDIR}/optimize_algo.py >>${LOG}