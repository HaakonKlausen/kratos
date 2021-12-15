#!/bin/bash
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../common.sh

writeKratosLog "INFO" "Starting Kratosdisplay"

# Disable Screensave
xset s 0
xset -dpms

# Start display
python3 ${PYTHONDIR}/kratosdisplay.py
