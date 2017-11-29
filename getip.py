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
import logging

#-------- My packages
from getipErrors import TimeoutGetIPError, BadDataGetIPError, UnknownIPSourceGetIPError, UnknownErrGetIPError

class GetIP_class:
    
    def __init__(self, args):
        self.logfile = args.logfile
        self.alertemail = args.alertemail
        self.debug = args.debug
        self.install = args.install
        self.ipfile = args.ipfile
        self.test = args.test
        
        # initiate logger
        formatstr = '%(asctime)s:%(levelname)s -> %(message)s' 
        loglevel = logging.INFO
        if (self.debug):
            loglevel = logging.DEBUG
            # We also print to stdout in debug mode!!
            logging.basicConfig(format=formatstr, level=loglevel, datefmt='%m/%d/%Y %I:%M:%S %p')
        else:
            logging.basicConfig(format=formatstr, level=loglevel, filename=self.logfile, datefmt='%m/%d/%Y %I:%M:%S %p')
            
    def exp(self):
        logging.debug("Debug message")
        logging.info("Number {} was chosen".format(1234))
        logging.warn("IP Changed!!")
        logging.error("OMG!!  Exception!!")
        logging.critical("Gack!")
        
        

# Set up args -----------------------------
description = "getIP v0.1\n"
description += "(c) 2017 Michael Rich (Twitter: @miketofet)\n"
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
ipgetter = GetIP_class(args)
ipgetter.exp()

