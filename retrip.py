# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 07:42:00 2017

retr[ieve]ip.py

This is the basic ip getter, meant to be called from another python module

Simply returns a string with the IP address

@author: MikeR
"""

#-------- Standard packages
import urllib2
import socket

#-------- My packages
from getipErrors import TimeoutGetIPError, BadDataGetIPError, UnknownIPSourceGetIPError, UnknownErrGetIPError

#-------- Basic function

def retrip_list():
    """
    Returns a list of sources available
    """
    slist = "ifconfig.me - IPv4 only"
    return slist

def retrip(source="ifconfig.me", ipv="IPv4"):
    """
    Wrapper to allow for alternate IP sources to be used.
    
    Will check the respone from a source and throw an error if it doesn't
    look like an IP address.
    """
    
    ip = "source not found"
    
    # Add new sources here
    if (source == "ifconfig.me"):
        ip = retrip_ifconfig(ipv)        
        
    if (ip == "source not found"):
        raise UnknownIPSourceGetIPError(source)
    
    if (not testip(ip, ipv)):
        raise BadDataGetIPError(source, ip, ipv)
        
    return ip
    
def testip(ip, ipv):
    """
    Using the socket package, try to convert provided data to a packed IP structure
    
    Socket throws errors if it won't work.
    
    The IPv6 functions ONLY work on *nix based systems and won't even run on a Windows machine
    
    returns True if IP data is good, False if bad
    """
    if (ipv == "IPv4"):
        try:
            socket.inet_aton(ip)
        except:
            # Only throws error on bad format to ip
            return False
    elif (ipv == "IPv6"):
        try:
            socket.inet_pton(socket.AF_INET6, ip)
        except:
            return False
    
    return True

#--------------- IP Source modules

def retrip_ifconfig(ipv):
    """
    Uses ifconfig.me to return my publically available IP address
    
    ifconfig.me/ip simpy returns the IP.  Nothing else.
    
    """
    if (ipv != "IPv4"):
        # ifconfig doesn't work with anything but ipv4
        raise UnknownErrGetIPError("retrip_ifconfig: Sorry ifconfig.me only returns IPv4 results")
    
    try:
        # UA: "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
        # Had to set it to match what my Firefox browser was putting out because ifconfig.me got ornery
        request = urllib2.Request("http://ifconfig.me/ip")
        opener = urllib2.build_opener()
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
        resp = opener.open(request).read().rstrip() 
        return resp
    except socket.timeout:
        # Recast as GetIPError
        raise TimeoutGetIPError("ifconfig.me")
    except BaseException as error:
        # Unknown
        raise UnknownErrGetIPError(error)
        