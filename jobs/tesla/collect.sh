#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Collecting Tesla data"
cd ${CONFIG}
#python3 ${PYTHONDIR}/get_tesla_info.py >>${LOG}
python3 ${PYTHONDIR}/tesla_api.py 