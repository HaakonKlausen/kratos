#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source ${DIR}/../common.sh

writeKratosLog "DEBUG" "Getting EUR exchange rate"
python3 ${PYTHONDIR}/collect_eur.py >>${LOG}