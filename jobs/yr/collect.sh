#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "INFO" "Collecting Yr Forecast data"
python3 ${PYTHONDIR}/collect_yr_forecast.py >>${LOG}
RETVAL=$?
if [ ${RETVAL} -eq 0 ]; then
    writeKratosLog "INFO" "Parsing Yr Forecast data..." >>${LOG}
    python3 ${PYTHONDIR}/parse_yr_forecast.py >>${LOG}
fi
