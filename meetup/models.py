#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Models for Meetup.com api
AUTHOR: dylangregersen
DATE: Mon Sep 15 00:12:21 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division
from django.db import models
from django.conf import settings
import datetime
import pytz
import warnings
from meetup.sync_utils import (fro_meetup_geo,to_meetup_geo,
                              fro_meetup_timestamp,to_meetup_timestamp)

DEFAULT_VIEW_TIMEZONE = pytz.timezone(getattr(settings,"TIME_ZONE","UTC"))

STATUS_OPTIONS = ("upcoming", "past", "proposed", "suggested", "cancelled", "draft")
VISIBILITY_OPTIONS = ("public", "public_limited","members")
JOIN_OPTIONS = ("open", "closed", "approval" )

# ########################################################################### #

class Mapper (object):
    """ Used to map names in two directions """

    def __init__ (self,name=""):
        self._to = {}
        self._from = {}
        self.name = name
        
    def __setitem__ (self,key,value):
        self._to[key] = value
        self._from[value] = key
        
    def __getitem__ (self,key):
        return self.to(key)
    
    def keys (self):
        return self._to.keys()
    
    def values (self):
        return self._to.values()
    
    def to (self,key):
        return self._to[key]

    def get_to (self,key,default=None):
        return self._to.get(key,default)

    def fro (self,value):
        return self._from[value]
        
    def get_fro (self,value,default=None):
        return self._from.get(value,default)
      
    def __iter__ (self):
        return iter(self._to.items()) 

class MeetupManager (models.Manager):  
          
    def _object_to_meetup_params (self,obj):
        mapper = self.meetup_mapper
        kws = {}
        field_names = [f.name for f in self.model._meta.fields]
        for field in field_names:            
            meetup_key = mapper.get_to(field,field)                
            kws[meetup_key] = getattr(obj,field)
        return self._post_object_to_meetup_params(obj,kws)
            
    def _post_object_to_meetup_params (self,obj,kws):
        return kws
        
    def _meetup_data_to_kws (self,meetup_data):
        mapper = self.meetup_mapper
        kws = {}
        field_names = [f.name for f in self.model._meta.fields]        
        for meetup_key in meetup_data:
            # map the meetup_key to the field name
            field = mapper.get_fro(meetup_key,meetup_key)
            # check the field name
            if field not in field_names:
                warnings.warn("ignoring meetup_key '{}' as field '{}'".format(meetup_key,field))
                continue
            # get the field values
            kws[field] = meetup_data[meetup_key]
        return self._post_meetup_data_to_kws(meetup_data,kws)
      
    def _post_meetup_data_to_kws (self,meetup_data,kws):
        return kws
     
    def _post_object_creation_or_update (self,obj,md):
        return obj
                
    def to_meetup_params (self,**filter):        
        """ Takes filters and converts each to meetup parameters 
        which a client who has permissions can POST via api.meetup.com        
        """                
        objs = self.filter(**filter)
        return [self._object_to_meetup_params(obj) for obj in objs]
      
    def from_meetup_data (self,meetup_data,sync=True):
        """ Takes Meetup data to model data
        
        Parameters
        meetup_data_kws : dict or list of dict
        sync : bool
            sync objects
            
        Parameters
        objects : list of objects OR list of dictionaries
            If sync is False then returns a list of the dictionary key/values to
            use to create or update the objects
            
        """            
        if isinstance(meetup_data,dict):
            meetup_data = [meetup_data]
        
        # primary key field name        
        pk_field = self.model._meta.pk.name
                
        objects = []
        for md in meetup_data:
            # get the key/value data from the meetup_data
            kws = self._meetup_data_to_kws(md)
            if sync:
                # create/update the group
                try:
                    obj = self.get(pk=kws[pk_field])
                    for key in kws:
                        setattr(obj,key,kws[key])
                    obj.save()
                except self.model.DoesNotExist:
                    obj = self.create(**kws)
                obj = self._post_object_creation_or_update(obj,md)
            else:
                # pass the key/value data through
                obj = kws
            objects.append(obj)
        return obj

pass
# ########################################################################### #

class VenueManager (MeetupManager):
    
    meetup_mapper = Mapper("venue_model -> meetup_data")
    
    def _post_meetup_data_to_kws (self,obj,kws):
        # convert longitude and latitude
        for key in ('lon','lat'):
            loc = fro_meetup_geo(kws.pop(key))
            if loc is not None:
                kws[key] = loc
        return kws
    
    def _post_object_to_meetup_params (self,meetup_data,kws):
        # convert longitude and latitude
        for key in ('lon','lat'):
            loc = to_meetup_geo(kws.pop(key))
            if loc is not None:
                kws[key] = loc
        return kws        
   
class Venue (models.Model):
    """ Meetup Venue Model """

    objects = VenueManager()
        
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128,blank=True)
    state = models.CharField(max_length=128,blank=True)
    country = models.CharField(max_length=128,blank=True)
    
    address_1 = models.CharField(max_length=128,blank=True)
    address_2 = models.CharField(max_length=128,blank=True)
    address_2 = models.CharField(max_length=128,blank=True)    
    
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
          
    def __unicode__ (self):
        return self.name 

    def view_location (self):
        return " ".join((self.address_1,self.city,self.state))
        
    def google_url (self):
        keywords = (self.name,self.city,self.state,self.country,self.address_1)
        search = "+".join(keywords).replace("/","_").replace(" ","+")
        # url = "https://www.google.com/search?q="+search
        url = "https://www.google.com/maps/place/"+search
        return url


class Member (models.Model):
    """ Meetup member account """
    member_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)        
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=33)
    created = models.DateTimeField()   
    updated = models.DateTimeField()
    visited = models.DateTimeField()    
    profile_url = models.URLField(max_length=255, blank=True) 
    
    def __unicode__(self):
        return self.name

class GroupManager (MeetupManager):
    
    meetup_mapper = Mapper("group_model -> meetup_data")
    meetup_mapper['n_members'] = 'members'
        
    def _post_meetup_data_to_kws (self,meetup_data,kws):
        # convert longitude and latitude
        for key in ('lon','lat'):
            loc = fro_meetup_geo(kws.pop(key,None))
            if loc is not None:
                kws[key] = loc      
        # if there are members then convert that number to an int
        key = str('n_members')
        if key in kws:
            kws[key] = int(kws[key] or 0)             
        
        # if timezone then check and convert to timezone string
        key = 'timezone'
        if key in kws:
            kws[key] = str(pytz.timezone(meetup_data[key])) 
                              
        return kws
    
    def _post_object_to_meetup_params (self,obj,kws):
        # convert longitude and latitude
        for key in ('lon','lat'):
            loc = to_meetup_geo(kws.pop(key))
            if loc is not None:
                kws[key] = loc
        kws['members'] = str(kws['members'])
        return kws        
                   
class Group (models.Model):
    """ Meetup Group Model """
    objects = GroupManager()
    
    VISIBLITY_CHOICES = VISIBILITY_OPTIONS
    
    name = models.CharField(max_length=128)
    urlname = models.CharField(max_length=128)
    city = models.CharField(max_length=128,blank=True)
    state = models.CharField(max_length=128,blank=True)
    country = models.CharField(max_length=128,blank=True)
    link = models.URLField()
    visibility = models.CharField(max_length=128,help_text="Visiblity to the users")
    timezone = models.CharField(max_length=128,blank=True)    
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)    
    n_members = models.IntegerField(default=0,blank=True) 
    who = models.CharField(max_length=128,blank=True)
    # join_mode = ('open',...)
    # category = ForeignKey   
    # topics = ForeignKey
    # photos = ...
    # organizer_id = ForeignKey
       
    def __unicode__ (self):
        return self.name
        
class EventManager(MeetupManager):
        
    meetup_mapper = Mapper("event_model_field -> meetup_data_key")
    meetup_mapper['event_timestamp'] = 'time'
        
    def _post_meetup_data_to_kws (self,meetup_data,kws):
        group_data = meetup_data['group']
        kws['group'] = Group.objects.from_meetup_data(group_data,sync=True)
        tzinfo = kws['group'].timezone                       
        key = self.meetup_mapper.fro('time')
        kws[key] = fro_meetup_timestamp(kws[key],tzinfo)
        return kws
    
    def _post_object_to_meetup_params (self,obj,kws):
        kws['time'],_ = to_meetup_timestamp(kws['time'])
        kws['group_id'] = obj.group.id        
        raise NotImplementedError("not sure if what data meetup wants back to change this")
        return kws        

    def _post_object_creation_or_update (self,obj,md):
        venue = Venue.objects.from_meetup_data(md['venue'],sync=True)
        obj.venue.add(venue)
        return obj
     
    def past(self):
        return Event.objects.filter(status='past')

    def upcoming(self):
        return Event.objects.filter(status='upcoming')

    def pending(self):
        return Event.objects.filter(status='pending')
      
class Event(models.Model): 
    """ Meetup Event Model """
    STATUS_OPTIONS = STATUS_OPTIONS
    VISIBILITY_OPTIONS = VISIBILITY_OPTIONS
    objects = EventManager()
    
    # Meetup.com fields
    event_url = models.URLField(max_length=255, blank=True)        
    name = models.CharField(max_length=255, blank=True)    
    status = models.CharField(max_length=16, choices=[(s,s) for s in STATUS_OPTIONS])
    visibility = models.CharField(max_length=16, choices=[(s,s) for s in VISIBILITY_OPTIONS])
    description = models.TextField(blank=True)    
    headcount = models.IntegerField(default=0,blank=True)
    yes_rsvp_count = models.IntegerField(default=0,blank=True)
    waitlist_count = models.IntegerField(default=0,blank=True)
    maybe_rsvp_count = models.IntegerField(default=0,blank=True)    
    
    event_timestamp = models.DateTimeField()  
    # fee_amount = float
    #  
    
    
    venue = models.ManyToManyField(Venue)
    group = models.ForeignKey(Group)

    # timezone to view event times in
    _view_tz = DEFAULT_VIEW_TIMEZONE 
    
    def __unicode__ (self):
        return self.name    
    
    def short_description(self, length=64):        
        desc = self.description[:length]
        if len(desc) == length:
            desc = desc[:-3] + "..."
        return desc    

    def set_view_tz (self,tz):
        if isinstance(tz,basestring):
            self._view_tz = pytz.timezone(tz)
        else:
            self._view_tz = tz 
    
    def get_view_tz (self):
        return getattr(self,'_view_tz',None)
      
    def _event_timestamp_in_view_tz (self,tz=None):
        dt = self.event_timestamp
        view_tz = self.get_view_tz()
        if tz is not None:  
            dt = dt.astimezone(tz)
        elif view_tz is not None:
            dt = dt.astimezone(view_tz)
        return dt        
    
    def view_status (self):
        return str(self.status)
    
    def view_when (self,tz=None):
        yr = self.view_year(tz)
        mo = self.view_month(tz)
        wd = self.view_weekday()
        day = self.view_day(tz)
        t = self.view_time_of_day(tz)        
        when = "{} {}".format(wd,mo)
        if str(datetime.datetime.today().year) != yr:
            when += " "+yr
        when += " {} at {}".format(day,t)
        return when    
    
    def view_month (self,tz=None):
        """ Event timestamp month string """
        mo = {1:"January",
                  2:"Febuary",
                  3:"March",
                  4:"April",
                  5:"May",
                  6:"June",
                  7:"July",
                  8:"August",
                  9:"September",
                  10:"October",
                  11:"November",
                  12:"December"}                                            
        dt = self._event_timestamp_in_view_tz(tz)
        return mo[dt.month]
        
    def view_day (self,tz=None):
        """ Event timestamp day of month """ 
        return str(self._event_timestamp_in_view_tz(tz).day)

    def view_year (self,tz=None):
        """ Event timestamp day of month """ 
        return str(self._event_timestamp_in_view_tz(tz).year)

    def view_weekday (self,tz=None):
        """ Event timestamp day of week string """    
        wk = {0:"Monday",
                  1:"Tuesday",
                  2:"Wednesday",
                  3:"Thursday",
                  4:"Friday",
                  5:"Saturday",
                  6:"Sunday"}
        dt = self._event_timestamp_in_view_tz(tz)                 
        return wk[dt.weekday()]

    def view_time_of_day (self,hour24=False,tz=None):
        dt = self._event_timestamp_in_view_tz(tz)
        h = dt.hour
        m = dt.minute        
        when = "{}:{:02}"
        if not hour24:
            if h < 12:                
                when += " AM"
            else:
                h -= 12
                when += " PM"        
        return when.format(h,m)




# class SurveyQuestionManager (MeetupManager)        
# class SurveyQuestion (models.Model):
# 
#     event = ForeignKey

    