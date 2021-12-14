#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "INFO" "Saving hourly DA data"
python3 ${PYTHONDIR}/get_hourly_powerprice.py >>${LOG}

