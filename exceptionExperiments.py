# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:44:18 2017

@author: MikeR
"""

import sys
from getipErrors import TimeoutGetIPError, BadDataGetIPError, UnknownIPSourceGetIPError, UnknownErrGetIPError
from time import sleep
import signal

try:
    raise TimeoutGetIPError("babab")
except TimeoutGetIPError as badnews:
    print "Unexpected error:", badnews
    print "host: ", badnews.host
    
try:
    f = open('noexist', 'r')
except IOError as error:
    print error
    if (error.errno == 2):
        print "yahhooo!"

go = True



def ctrlc(signal, frame):
    print "crtlc: setting go to False"
    global go
    go = False

def lightsleeper(s):
    """
    This will sleep for s seconds, but allow for IO every second.
    This introduces error into the timing.
    
    """
    global go
    for i in range(s):
        sleep(1)
        if (not go): return
        
    
signal.signal(signal.SIGINT, ctrlc)
count = 0
while (go):
    print "Sleeping for 3 seconds"
    sleep(3)
    count += 1
    if (count > 10):
        go = False

print "Exited loop"

        