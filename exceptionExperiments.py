# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:44:18 2017

@author: MikeR
"""

import sys

try:
    thing = 1/0
except BaseException as badnews:
    print "Unexpected error:", badnews
    
