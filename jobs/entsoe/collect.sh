#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG=${HOME}/log/kratos.log
NOW=$(date)
echo "${NOW} Collecting DA data..." >>${LOG}
${DIR}/collect_da.py >>${LOG}
RETVAL=$?
if [ ${RETVAL} -eq 0 ]; then
    echo "${NOW} Parsing DA data..." >>${LOG}
    ${DIR}/parse_da.py >>${LOG}
fi