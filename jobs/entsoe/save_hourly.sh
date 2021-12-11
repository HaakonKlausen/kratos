#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG=${HOME}/log/kratos.log
NOW=$(date)
echo "${NOW} Saving hourly DA data..." >>${LOG}
${DIR}/get_hourly_powerprice.py >>${LOG}
