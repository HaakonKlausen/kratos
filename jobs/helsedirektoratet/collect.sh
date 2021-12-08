#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LOG=${HOME}/log/kratos.log
NOW=$(date)
echo "${NOW} Collectiong Covid Admission data..." >>${LOG}
${DIR}/collect_covid_admissions.py >>${LOG}
