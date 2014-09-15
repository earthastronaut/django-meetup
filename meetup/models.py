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
import datetime
import pytz
import warnings
from meetup.sync_utils import (fro_meetup_geo,to_meetup_geo,
                              fro_meetup_timestamp,to_meetup_timestamp)

STATUS_CHOICES = ('past','pending','upcoming')
VISIBILITY_CHOICES = ('public','private')

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
          
    def _object_to_meetup_data (self,obj):
        mapper = self.meetup_mapper
        kws = {}
        field_names = [f.name for f in self.model._meta.fields]
        for field in field_names:            
            meetup_key = mapper.get_to(field,field)                
            kws[meetup_key] = getattr(obj,field)
        return self._post_object_to_meetup_data(obj,kws)
            
    def _post_object_to_meetup_data (self,obj,kws):
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
                
    def to_meetup_data (self,**filter):        
        """ Takes filters and converts each to meetup data """                
        objs = self.filter(**filter)
        return [self._object_to_meetup_data(obj) for obj in objs]
      
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
            loc = to_prep_geo(kws.pop(key))
            if loc is not None:
                kws[key] = loc
        return kws
    
    def _post_object_to_meetup_data (self,meetup_data,kws):
        # convert longitude and latitude
        for key in ('lon','lat'):
            loc = fro_prep_geo(kws.pop(key))
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
        key = str('n_members')
        if key in kws:
            kws[key] = int(kws[key] or 0)        
        return kws
    
    def _post_object_to_meetup_data (self,obj,kws):
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
    
    VISIBLITY_CHOICES = VISIBILITY_CHOICES
    
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
        
    meetup_mapper = Mapper("event_model -> meetup_data")
    meetup_mapper['timestamp'] = 'time'
        
    def _post_meetup_data_to_kws (self,meetup_data,kws):
        group_data = meetup_data['group']
        kws['group'] = Group.objects.from_meetup_data(group_data,sync=True)
        tzinfo = kws['group'].timezone               
        kws['timestamp'] = fro_meetup_timestamp(kws['timestamp'],tzinfo)
        return kws
    
    def _post_object_to_meetup_data (self,obj,kws):
        kws['time'],_ = to_meetup_timestamp(kws['time'])
        kws['group_id'] = obj.group.id        
        raise NotImplementedError("not sure if what data meetup wants back to change this")
        return kws        
            
    def past(self):
        return Event.objects.filter(status='past')

    def upcoming(self):
        return Event.objects.filter(status='upcoming')

    def pending(self):
        return Event.objects.filter(status='pending')
      
class Event(models.Model): 
    """ Meetup Event Model """
    STATUS_CHOICES = STATUS_CHOICES
    VISIBILITY_CHOICES = VISIBILITY_CHOICES
    objects = EventManager()
    
    # Meetup.com fields
    event_url = models.URLField(max_length=255, blank=True)        
    name = models.CharField(max_length=255, blank=True)    
    status = models.CharField(max_length=16, choices=[(s,s) for s in STATUS_CHOICES])
    visibility = models.CharField(max_length=16, choices=[(s,s) for s in VISIBILITY_CHOICES])
    description = models.TextField(blank=True)
    
    headcount = models.IntegerField(default=0,blank=True)
    yes_rsvp_count = models.IntegerField(default=0,blank=True)
    waitlist_count = models.IntegerField(default=0,blank=True)
    maybe_rsvp_count = models.IntegerField(default=0,blank=True)    
    
    timestamp = models.DateTimeField()    

    venue = models.ManyToManyField(Venue)
    group = models.ForeignKey(Group)

    def __unicode__ (self):
        return self.name    
    
    def short_description(self, length=64):        
        desc = self.description[:length]
        if len(desc) == length:
            desc = desc[:-3] + "..."
        return desc    


        
    
    