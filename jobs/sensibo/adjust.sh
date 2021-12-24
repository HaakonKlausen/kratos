#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Sensibo Adjust running"
python3 ${PYTHONDIR}/sensibo_control.py adjust >>${LOG} 2>>${LOG}