#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG=${HOME}/log/kratos.log
NOW=$(date)
echo "${NOW} Collectiong Telldus sensor data..." >>${LOG}
${DIR}/collect_sensor_data.py --kratosdata >>${LOG}

