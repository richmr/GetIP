# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:44:18 2017

@author: MikeR
"""

import sys
from getipErrors import TimeoutGetIPError, BadDataGetIPError, UnknownIPSourceGetIPError, UnknownErrGetIPError

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
        