#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Collection weConnect data"
python3 ${PYTHONDIR}/collect_weconnect.py >>${LOG} 2>>${LOG}