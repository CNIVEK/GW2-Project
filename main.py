################################################################################
# Main appliaction script
#
# Purpose: This application displays various information on daily achievements.
# Users can choose to either display today’s or tomorrow’s achievements. They
# will also be able to optionally request specific category of achievement
# (pve, pvp, wvw, fractals, special) corresponding to the day. When the options
# are defined, the application will utilize the Guild Wars 2 API to gather
# information. Relevant information will then be filtered into a report. Reports
# are saved into in a Redis Labs database. Reports are then retrieved from the
# database and displayed to the console.
#
# This script runs the the application using the facade object (SystemWrapper).
# This program is designed to be a subsystem and is intended to be used for a
# larger application
#
# Author: Kevin Chen
# Contact: chenk106@mcmaster.ca
# GitHub: https://github.com/CNIVEK/GW2-Project
#
################################################################################

from systemwrapper import *

subsystem_daily = SystemWrapper()
subsystem_daily.daily()
