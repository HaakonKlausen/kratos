#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "INFO" "Collecting Telldus sensor data"
python3 ${PYTHONDIR}/collect_sensor_data.py --kratosdata >>${LOG}
