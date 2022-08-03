#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

# Store PID
echo $BASHPID >${CONFIG}/read-oss-aidon.pid 

# Restart in case it stops
while true
do
	writeKratosLog "INFO" "Starting Read Oss-Brikken app for Aidon"
	python3 ${PYTHONDIR}/read_oss_aidon.py >>${LOG} 2>>${LOG}
	writeKratosLog "WARN" "Read Oss-Brikken app for Aidon aborted"
done