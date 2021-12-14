#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source ${DIR}/../common.sh

writeKratosLog "INFO" "Collectiong Covid Admission data"
python3 ${PYTHONDIR}/collect_covid_admissions.py >>${LOG}
