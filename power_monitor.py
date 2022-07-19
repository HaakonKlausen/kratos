#!/usr/bin/python3
#
# To be run every minute, checking current power usage and limit if needed
# Priority stop:
# - Turn down AC 
# - Water heater
# - Car charger
# - Living room heater
# Test comment.

import datetime
import pytz
import sys
import time 

from configobj import ConfigObj

import kratoslib

