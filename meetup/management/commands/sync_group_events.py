#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Sync Meetup group events to local database
AUTHOR: dylangregersen
DATE: Mon Sep 15 00:54:16 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division, unicode_literals
import os 
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from meetup.sync import sync_group_events
from meetup.api import MeetupClient

MEETUP_KEY =  settings.MEETUP_KEY

# ########################################################################### #

class Command(BaseCommand):
    help = 'Sync Meetup group events to local database'

    def add_arguments(self, parser):
        parser.add_argument('group_id', nargs='+', type=int,help="group id, default is settings.MEETUP_GROUP_ID")
        parser.add_argument('--api_key',type=str,help="Key used for querying Meetup")        
                    
    def handle(self, *args, **options):
        client = MeetupClient(options.get('api_key',MEETUP_KEY))
        # ======================= get the group
        if len(args) == 1:
            group_id = int(args[0])
        else:        
            group_id = settings.MEETUP_GROUP_ID
        # ======================= sync events for the group            
        sync_group_events(group_id,client)
        