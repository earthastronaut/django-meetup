#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: For testing syncing utilities
AUTHOR: dylangregersen
DATE: Mon Sep 15 00:52:58 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division, unicode_literals
import os 
from unittest import TestCase
from meetup.sync_utils import fro_meetup_timestamp
import unittest

# ########################################################################### #

# TODO: implement tests

class TestMeetupConversions (TestCase):
    
    def setUp(self):
        pass 
        
    def test_parse_meetup_time ():
        meetup_time = 1411338964000.0        
        sol = datetime.datetime(2014,9,21,16,36,4,tzinfo=pytz.timezone("US/Mountain"))
        # pass in tz as string
        tzinfo = "US/Mountain"
        ans = fro_meetup_timestamp(meetup_time,tzinfo)
        assert sol == ans 

    def test_parse_meetup_time_tzinfo ():
        meetup_time = 1411338964000.0        
        sol = datetime.datetime(2014,9,21,16,36,4,tzinfo=pytz.timezone("US/Mountain"))    
        # pass in timezone as object
        tzinfo = pytz.timezone("US/Mountain")
        ans = fro_meetup_timestamp(meetup_time,tzinfo)
        assert sol == ans 
            
    def test_to_meetup_timestamp ():        
        d = datetime.datetime(2014,9,21,16,36,4,tzinfo=pytz.timezone("US/Mountain"))
        sol = 1411338964000.0   
        ans = to_meetup_timestamp(d)
        assert sol == ans 
                
    def test_geo_stamp ():
        pass


pass 
# ########################################################################### #
if __name__ == "__main__":
    pass
    
