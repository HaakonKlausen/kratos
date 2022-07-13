#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

pid=$(cat ${CONFIG}/read-oss-aidon.pid)
count=$(ps -e | grep ${pid} | grep read-oss-aid | wc -l)

if [ $count -ne 0 ]; then
	writeKratosLog "DEBUG" "Read Oss Aidon Job is running, no need to start"
	exit 0
fi
writeKratosLog "INFO" "Starting Read Oss Aidon Job"
nohup ${DIR}/read-oss-aidon.sh >/dev/null 2>/dev/null &