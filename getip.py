# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 14:38:48 2017

This is designed to be run as a cron job to check the public ip for a server
The frequency of use is up to the cron settings, but the install argument will 
put this in the daily cron jobs

Arguments:
    --install - Final install of the work when complete
    -l, --logfile - Logfile
    --debug - Ensure highest level of logging
    -i, --ipfile - Designate the file to look for current ip
    --alertemail - Designate email recipient to get an alert if detected external ip changes.
    --test - Launch getip in test mode, where it will check the ip every [s] seconds and not exit. 


@author: MikeR
"""

#-------- Standard packages
import argparse

#-------- My packages
from getipErrors import TimeoutGetIPError, BadDataGetIPError, UnknownIPSourceGetIPError, UnknownErrGetIPError



# Set up args -----------------------------
description = "getIP v0.1\n"
description += "Detects and logs the current external IP of a system.  Intended for use on home-based servers."

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-l', '--logfile', type=str, default='/var/log/getip/getip.log', help='Designate the logfile. Default is /var/log/getip/getip.log')
parser.add_argument('-i', '--ipfile', type=str, default='/var/log/getip/.currentip', help='Designate the file where the last detected IP is stored.  Default is /var/log/getip/.currentip')
parser.add_argument('--debug', action='store_true', help='Enable all debugging log messages')
onceAnHour = 60*60
parser.add_argument('--test', type=int, default=onceAnHour, help='Launch getip in test mode.  Getip will check the IP every t seconds.  Default is once an hour.  This also enable --debug')
parser.add_argument('--install', action='store_true', help='Install getip.  Run as root.')
parser.add_argument('--alertemail', type=str, help='Designate the email to receive an alert when the public IP changes')

# And GO!

args = parser.parse_args()