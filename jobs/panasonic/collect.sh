#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "INFO" "Fetching Panasonic heat pump info"
if [ -f "/home/pi/.panasonic-token" ]; then
	python3 ${PYTHONDIR}/panasonic_control.py storeinfo >>${LOG} 2>>${LOG}
else
	writeKratosLog "ERROR" "Panasonic token expired"
fi
