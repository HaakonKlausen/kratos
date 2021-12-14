#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "INFO" "Collecting DA data"
python3 ${PYTHONDIR}/collect_da.py >>${LOG}
RETVAL=$?
if [ ${RETVAL} -eq 0 ]; then
    writeKratosLog "INFO" "Parsing DA data"
    python3 ${PYTHONDIR}/parse_da.py >>${LOG}
fi
