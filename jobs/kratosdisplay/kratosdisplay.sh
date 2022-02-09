#!/bin/bash
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh



# Disable Screensave
xset s 0
xset -dpms

# Start display
while true
do
	writeKratosLog "INFO" "Starting Kratosdisplay"
	python3 ${PYTHONDIR}/kratosdisplay.py >>${LOG} 2>>${LOG}
	writeKratosLog "WARN" "Kratosdisplay exited, restarting"
done
