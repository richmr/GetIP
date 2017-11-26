# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 07:42:00 2017

retr[ieve]ip.py

This is the basic ip getter, meant to be called from another python module

Simply returns a string with the IP address

@author: MikeR
"""

import urllib2


#-------- Basic function

def retrip(source="ifconfig.me", ipv="IPv4"):
    """
    Wrapper to allow for alternate IP sources to be used.
    
    Will check the respone from a source and throw an error if it doesn't
    look like an IP address.
    """
    
    ip = "not an IP"
    
    # Add new sources here
    if (source == "ifconfig.me"):
        ip = retrip_ifconfig(ipv)
        testip(ip, ipv)
        return ip
    
    