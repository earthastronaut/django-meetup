#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Utilities for converting to and from Meetup data 
AUTHOR: dylangregersen
DATE: Mon Sep 15 09:18:17 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division, unicode_literals
import os 
import time
import datetime
import pytz

# ########################################################################### #

def fro_meetup_geo (geo):
    """ From Meetup Data to geo location"""
    if geo is None or not geo:
        return 
    return float(geo)
    
def to_meetup_geo (geo):
    """ from geo location to Meetup data geo """
    return geo
    
def fro_meetup_timestamp (t,tzinfo):
    struct_time = time.gmtime(int(t) / 1000.0)    
    keys = ['year','month','day','hour','minute','second']
    kws = {k:struct_time[i] for i,k in enumerate(keys)}
    kws['tzinfo'] = pytz.timezone(tzinfo)   
    return datetime.datetime(**kws)

def to_meetup_timestamp (ts):
    tzinfo = str(ts.tzinfo)
    t = time.mktime(d.timetuple())
    return t,tzinfo

