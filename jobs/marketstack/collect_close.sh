#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Collecting Close Marketstack data"
python3 ${PYTHONDIR}/collect_marketstack_close.py >>${LOG}
