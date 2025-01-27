#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Fetching Panasonic heat pump history"
python3 ${PYTHONDIR}/collect_heatpump_power.py >>${LOG} 2>>${LOG}

