# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 14:38:48 2017

Defines exceptions raised when this code runs

Follows pattern shown in: https://docs.python.org/2/tutorial/errors.html#tut-userexceptions

@author: MikeR
"""

class GetIPError(Exception):
    """Base class for exceptions in the GetIP module."""
    pass

class TimeoutGetIPError(GetIPError):
    """
    Exception raised when an attempt takes too long

    Attributes:
        host -- host that took too long
    """

    def __init__(self, host):
        self.host = host
        

class BadDataGetIPError(GetIPError):
    """
    Raised when host, after parsing, does not provide an IP string

    Attributes:
        host -- host that returned the data
        retdata -- sample of returned data (just 50 bytes for review)
        ipv  -- What IPvX version we were looking for
    """

    def __init__(self, host, retdata, ipv):
        self.host = host
        self.retdata = retdata[:50]
        self.ipv = ipv

class UnknownIPSourceGetIPError(GetIPError):
    """
    Raised if retrip called with an unknown IP data source
    
    Attributes:
        host -- host that was asked for
    """
    def __init__(self, host):
        self.host = host
       
class UnknownErrGetIPError(GetIPError):
    """
    Raised on unknown responses from underlying packages
    
    Attributes:
        msg = Data from the unknown error
    """
    def __init__(self, msg):
        self.msg = msg