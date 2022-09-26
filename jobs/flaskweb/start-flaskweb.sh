#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

pid=$(cat ${CONFIG}/flaskweb.pid)
count=$(ps -e | grep ${pid} | grep flaskweb | wc -l)

if [ $count -ne 0 ]; then
	writeKratosLog "DEBUG" "Flaskweb Job is running, no need to start"
	exit 0
fi
writeKratosLog "INFO" "Starting Flaskweb Job"
nohup ${DIR}/flaskweb.sh >/dev/null 2>/dev/null &