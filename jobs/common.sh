#!/bin/bash
#
# Common functions and env variables
#
COMMONDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHONDIR=${COMMONDIR}/../kratos
LOG=${HOME}/.config/kratos/kratos.log

writeKratosLog () {
	severity=$1
	message=$2
	NOW=$(date)
	echo "${NOW} Job ${severity}: ${message}" >>${LOG}
}