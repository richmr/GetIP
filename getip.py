#!/usr/bin/python

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
import smtplib
from email.mime.text import MIMEText
import socket
from time import sleep
import signal

#-------- My packages
import retrip
from getipErrors import TimeoutGetIPError, BadDataGetIPError, UnknownIPSourceGetIPError, UnknownErrGetIPError

class GetIP_class:
    
    def __init__(self, args):
        self.logfile = args.logfile
        self.alertemail = args.alertemail
        self.debug = args.debug
        self.install = args.install
        self.ipfile = args.ipfile
        self.test = args.test
        self.list = args.list
        self.source = args.source
        self.ipv = "IPv6" if args.ipv6 else "IPv4"
        self.stop = False
        
        if (self.test):
            self.debug=True
              
        
        
            
    def exp(self):
        logging.debug("Debug message")
        logging.info("Number {} was chosen".format(1234))
        logging.warn("IP Changed!!")
        logging.error("OMG!!  Exception!!")
        logging.critical("Gack!")
        
    def sendAlertEmail(self, subject, body):
        try:
            msg = MIMEText(body)
            to = self.alertemail
            frm = "getip"
            msg['Subject'] = subject
            msg['From'] = frm
            msg['To'] = to
            s = smtplib.SMTP('localhost')
            s.sendmail(frm, [to], msg.as_string())
            s.quit()
            logging.info("Email sent to {}".format(to))
        except BaseException as badnews:
            logging.error("Failed to send alert email because: {}".format(badnews))     
            
    def sighandle(self, signal, frame):
        logging.debug("SIGINT received.")
        self.stop = True
        
    
    def start(self):
        if (self.list):
            print "Available IP data sources:"
            print "--------------------------"
            print "{}".format(retrip.retrip_list())
            return
        
        # initiate logger
        formatstr = '(%(asctime)s) %(levelname)s-> %(message)s'
        datefmtstr = '%m/%d/%Y %H:%M:%S'
        loglevel = logging.INFO
        if (self.debug):
            loglevel = logging.DEBUG
            # We also print to stdout in debug mode!!
            logging.basicConfig(format=formatstr, level=loglevel, datefmt=datefmtstr)
        else:
            logging.basicConfig(format=formatstr, level=loglevel, filename=self.logfile, datefmt=datefmtstr)
        
        if (self.test):
            logging.debug("Entering test mode.  Will check IP using source {} once every {} seconds".format(self.source, self.test))
            signal.signal(signal.SIGINT, self.sighandle)
            while (not self.stop):
                self.go()
                sleep(self.test)
        else:
            self.go()
    
    def go(self):
        # Start try block
        try:
            logging.debug("getip.go: Started try block")
            currentip = retrip.retrip(self.source, self.ipv)
            logging.info("Source {} returned IP: {}".format(self.source, currentip))
            
            #Check the ipfile for last ip
            try:
                f = open(self.ipfile, 'r')
                oldip = f.readline().strip()
                f.close()
                if (oldip == currentip):
                    logging.info("New IP: {} matches old IP {}.".format(currentip, oldip))
                else:
                    logging.warn("New IP: {} does NOT match old IP: {}.  Reset your DNS records!".format(currentip, oldip))
                    if (self.alertemail):
                        logging.debug("Attempting to send alert email to: {}".format(self.alertemail))
                        self.sendAlertEmail("IP address change!!", "The IP address for {} has changed to {}".format(socket.gethostname(), currentip))
                    # reopen file to overwrite
                    f = open(self.ipfile, 'w')
                    logging.debug("opened ipfile for writing")
                    f.write(currentip + "\n")
                    f.close()
                    logging.debug("wrote {} to ipfile".format(currentip))
            except IOError as badnews:
                try:
                    if (badnews.errno == 2):
                        # No existing ip file
                        logging.info("No existing ipfile, establishing initial entry with ip = {}".format(currentip))
                        f = open(self.ipfile, 'w')
                        logging.debug("opened ipfile for writing")
                        f.write(currentip + "\n")
                        f.close()
                        logging.debug("wrote {} to ipfile".format(currentip))
                    else:
                        logging.error("Failed ipfile check because: {}".format(badnews))
                except BaseException as rllybadnews:
                    logging.error("Failed to create initial ipfile because: {}".format(rllybadnews))
            except BaseException as badnews:
                logging.error("Failed ipfile check because: {}".format(badnews))
        
        # Failures to get ip                        
        except TimeoutGetIPError as timeout:
            logging.error("Timeout while trying to get data from: {}".format(timeout.host()))
            # Really should retry several times and then send alert email, but not putting this in here
        except BadDataGetIPError as baddata:
            logging.error("Source {} returned bad data that looked like: {}".format(baddata.host, baddata.retdata))
            # email?
        except UnknownIPSourceGetIPError as unksource:
            logging.error("Source {} is not valid!".format(unksource.host))
        except UnknownErrGetIPError as unkerr:
            logging.error("getip failed because: {}".format(unkerr.msg))
        except BaseException as badnews:
            logging.error("getip failed because: {}".format(badnews.msg))
            
# End GetIP_class def

# Set up args -----------------------------
description = "getIP v0.1\n"
description += "(c) 2017 Michael Rich (Twitter: @miketofet)\n"
description += "Detects and logs the current external IP of a system.  Intended for use on home-based servers."

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-l', '--logfile', type=str, default='/var/log/getip/getip.log', help='Designate the logfile. Default is /var/log/getip/getip.log')
parser.add_argument('-i', '--ipfile', type=str, default='/var/log/getip/.currentip', help='Designate the file where the last detected IP is stored.  Default is /var/log/getip/.currentip')
parser.add_argument('--debug', action='store_true', help='Enable all debugging log messages')
parser.add_argument('--test', type=int, help='Launch getip in test mode.  Getip will check the IP every t seconds.  This also enable --debug')
parser.add_argument('--alertemail', type=str, help='Designate the email to receive an alert when the public IP changes')
parser.add_argument('--source', type=str, default="ifconfig.me", help="Designate source of ip data.  Use --list to see a list of sources")
parser.add_argument('--list', action='store_true', help='Get a list of possible ip data sources')
parser.add_argument('--ipv6', action='store_true', help='Retrieve a IPv6 result, not IPv4.')
# And GO!

args = parser.parse_args()
ipgetter = GetIP_class(args)
ipgetter.start()

