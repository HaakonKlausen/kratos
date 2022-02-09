#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Prototype running"
python3 ${PYTHONDIR}/prototype.py >>${LOG} 2>>${LOG}