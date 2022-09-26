#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

# Store PID
echo $BASHPID >${CONFIG}/flaskweb.pid 

# Restart in case it stops
while true
do
	writeKratosLog "INFO" "Starting Flaskweb"
	cd ${PYTHONDIR}
	export FLASK_APP=flaskweb.py
	export FLASK_ENV=development
	flask run >>${LOG} 2>>${LOG}
	writeKratosLog "WARN" "Flaskweb aborted, restarting"
done