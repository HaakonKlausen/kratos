#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "INFO" "Collecting Live Marketstack data"
python3 ${PYTHONDIR}/collect_marketstack_live.py >>${LOG}
