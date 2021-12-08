#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG=${HOME}/log/kratos.log
NOW=$(date)
echo "${NOW} Collecting Yr Forecast data..." >>${LOG}
${DIR}/collect_yr_forecast.py >>${LOG}
${DIR}/parse_yr_forecast.py >>${LOG}