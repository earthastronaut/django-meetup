#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Methods and functions to assist-viewing/view content
AUTHOR: dylangregersen
DATE: Tue Sep 16 08:40:49 2014
"""
# ########################################################################### #

from __future__ import print_function, division, unicode_literals
from django.conf import settings
from django.shortcuts import render,render_to_response
from meetup.models import Venue,Group,Event
from django.template import RequestContext

MEETUP_GROUP_ID = getattr(settings,"MEETUP_GROUP_ID",None)

# ########################################################################### #

def next_group_event (group=MEETUP_GROUP_ID,**filter):
    """ Recover the next upcoming event for a group
    
    default group is from ``django.conf.settings.MEETUP_GROUP_ID``. If None then
    you will have to give the group explicitly when calling this function
    
    Parameters
    ----------
    group : Group.object or Group.object.pk
    filter : dict
        Refine the Event.objects.filter(**filter) call
    
    Returns
    -------
    next : single Event.object or None
    
    """
    filter['status'] = 'upcoming'
    filter['group'] = Group.objects.get(pk=group)        
    events = Event.objects.filter(**filter).order_by("-event_timestamp")
    n = len(events)
    if n > 0:
        return events[n-1]

def view_upcoming_past_events (request):
    context = RequestContext(request)
    group_id = MEETUP_GROUP_ID
    
    group = Group.objects.get(pk=group_id)
    
    events = list(Event.objects.order_by("-event_timestamp").filter(status="upcoming",group=group_id))
    events += list(Event.objects.order_by("-event_timestamp").filter(status="past",group=group_id))
    venues = [e.venue.get() for e in events]
    
    context_dict = dict()
    context_dict['events_venues'] = zip(events,venues)
    context_dict['group'] = group
    
    return render_to_response("meetup/events.html",context_dict,context)

def view_next_event (template):
    def render_view (request):
        context = RequestContext(request)    
        context_dict = dict(next_group_event=next_group_event())
        return render_to_response(template,context_dict,context)

# NOTES:
# 
# * Filter events : the ``status`` field uses useful "upcoming","past","pending" keywords
# which you can filter by using Event.objects.filter(status="upcoming")
#

# ########################################################################### #
