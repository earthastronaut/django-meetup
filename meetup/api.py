#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PURPOSE: Tools to access the Meetup.com API
AUTHOR: dylangregersen
DATE: Mon Sep 15 00:12:21 2014
"""
# ########################################################################### #

# import modules 

from __future__ import print_function, division, unicode_literals
import os
from urllib import urlencode
from urllib2 import urlopen
try:
    import json
except ImportError:
    import simplejson as json

# ########################################################################### #

class MeetupClient(object):
    """ MeetupClient """
    def __init__(self, api_key):
        """ Find your api_key from https://secure.meetup.com/meetup_api/key/"""
        self.api_key = api_key    
        self._cached_request_urls = {}
        
    def signed_request_url (self,meetup_method,params=None,request_hash=None):
        """ To GET data from api.meetup.com 
        
        """        
        if request_hash is not None and request_hash in self._cached_request_urls:
            return self._cached_request_urls[request_hash]
        
        # get the parameters 
        params = params.copy() if params is not None else {}
        params['signed'] = True

        response = self.invoke(meetup_method,params,method='GET')
        signed_url = response['signed_url']
        if request_hash is not None:
            self._cached_request_urls[request_hash] = signed_url
        return signed_url
    
    def invoke (self, meetup_method, params=None, method='GET'):
        """ For invoking a request
        
        Parameters
        meetup_method : string
            see http://www.meetup.com/meetup_api/docs/
        params : dict or None
            parameters passed to the request                    
        method : string  
            'GET' or 'POST'
        
        Returns
        response : dict
        
        """
        # TODO: rename invoke to http_response        
        
        # get the parameters 
        params = params.copy() if params is not None else {}
        params['key'] = self.api_key
        params['page'] = 1000
                
        # the specific meetup method
        # see http://www.meetup.com/meetup_api/docs/
        if meetup_method.startswith("/"):
            meetup_method = meetup_method[1:]        
        url =  os.path.join("https://api.meetup.com",meetup_method)
        
        # get response
        if method == 'GET':
            return self._get(url, params)
        elif method == 'POST':
            return self._post(url, params)
    
    def _get(self, url, params):
        url = "{}?{}".format(url, urlencode(params))
        content = urlopen(url).read()
        content = unicode(content, 'utf-8', 'ignore')
        return json.loads(content)
        
    def _post(self, url, params):
        content = urlopen(url, urlencode(params)).read()
        content = unicode(content, 'utf-8', 'ignore')
        return json.load(content)
        
    def get_events (self,id,id_type="group",**params):
        params = params.copy()
        params.setdefault('status',"upcoming,past,pending")
        params['{}_id'.format(id_type)] = id
        return self.invoke("2/events",params)
        
    def update_event(self, event_id, **params):
        return self.invoke('event/{}'.format(event_id), params, method='POST')

