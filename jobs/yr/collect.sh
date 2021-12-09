#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG=${HOME}/log/kratos.log
NOW=$(date)
echo "${NOW} Collecting Yr Forecast data..." >>${LOG}
${DIR}/collect_yr_forecast.py >>${LOG}
RETVAL=$?
if [ ${RETVAL} -eq 0 ]; then
    echo "${NOW} Parsing Yr Forecast data..." >>${LOG}
    ${DIR}/parse_yr_forecast.py >>${LOG}
fi