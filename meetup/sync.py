#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: methods for syncing meetup.models with api.meetup.com data 
AUTHOR: dylangregersen
DATE: Mon Sep 15 00:12:21 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division, unicode_literals
from django.conf import settings
from meetup.api import MeetupClient
from meetup.models import Venue, Group, Event, STATUS_OPTIONS

MEETUP_KEY =  settings.MEETUP_KEY

# ########################################################################### #

def sync_group_events (group_id,client=None):
    """ Use meetup group id to sync all events to this data base """
    if client is None:
        client = MeetupClient(MEETUP_KEY)
    # ======================= get the group
    params = {}
    params['group_id'] = group_id
    results = client.invoke("/2/groups",params=params)['results']
    if not len(results):
        raise ValueError("No meetup group_id {}".format(params['group_id']))
    
    # ======================= sync events for the group    
    for group_data in results:
        # create group
        group = Group.objects.from_meetup_data(group_data)
        print(" -- for group {} --".format(group.name))
        # get all status options
        params['status'] = ",".join(STATUS_OPTIONS) 
        events = client.invoke("/2/events",params)['results']
        for event_data in events:                    
            event = Event.objects.from_meetup_data(event_data)
            print("   -- sync event {} --".format(event.name))                

