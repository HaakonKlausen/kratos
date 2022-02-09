#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

pid=$(cat ${CONFIG}/read-oss-kamstrup.pid)
count=$(ps -e | grep ${pid} | grep read-oss-kam | wc -l)

if [ $count -ne 0 ]; then
	writeKratosLog "DEBUG" "Read Oss Kamstrup Job is running, no need to start"
	exit 0
fi
writeKratosLog "INFO" "Starting Read Oss Kamstrup Job"
nohup ${DIR}/read-oss-kamstrup.sh >/dev/null 2>/dev/null &