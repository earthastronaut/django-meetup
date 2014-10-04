Django-Meetup
=============

This is a general purpose django-app for syncing Meetup.com to a local database and adding Meetup.com content to a website.

This was specifically designed to put events for one Meetup.com group onto their independent website. However, it was designed to give flexibility to the developer for whatever Meetup.com content syncing and posting they wish. 

To use
------

Install via pip

.. code-block:: bash

    pip install django-meetup

Add to your Django settings module the following variables

.. code-block:: python 
    
    THIRD_PARTY_APPS = [ 
        ...,
        "meetup",
        ...,
    ]
    
    MEETUP_KEY = ""
    
    # **Security Warning:** Keep personal Meetup api key secret.
    # Read `Meetup documentation <https://secure.meetup.com/meetup_api/key/>`_.
    
    MEETUP_GROUP_ID = 123456789
    
    # (optional) This is the default group id to get information fro      
        
    MEETUP_ALLOW_ADMIN = True

    # (optional) This boolean will set up admin interface. 
    # **WARNING:** Methods to sync TO Meetup have not been completed. 
    #    So any changes to the database are local.
 
    TIME_ZONE = "UTC"
    
    # (optional) This key is standard Django. The meetup package stores times 
    # in "UTC" but methods to view the time will set to TIME_ZONE as the default
    # for that view 
    

To sync group events 
--------------------

To sync up a group, from the command line run
    
.. code-block:: bash    
    
    py manage.py sync_group_events <group_id>

How it works
------------

`Meetup.com <https://www.meetup.com>`_. provides an api which a Meetup.com member can access via `api.meetup.com <https://api.meetup.com>`_..

This package implements a MeetupClient which uses a meetup member's `meetup api key <https://secure.meetup.com/meetup_api/key/>`_.. The client can query the meetup api and get back dictionaries of "meetup data". Note that member permissions on Meetup.com apply to the members api queries.

Models made to mimic hypothesized meetup.com database tables can take the client's data and turn them into local database objects.

The developer can then use the models to post information onto their webpage.

To contribute
-------------

If you have methods or modifications which refine this package please contribute via `github astrodsg/django-meetup <https://github.com/astrodsg/django-meetup.git>`_.

Other resources
---------------

Other resources to consider for requesting/posting data from Meetup.com

* `python-api-client <https://github.com/meetup/python-api-client>`_..

* `signed requests using javascript <http://www.meetup.com/meetup_api/auth/#keysign>`_..


Note: In the project I developed this for I decided to go with a smaller app which doesn't store local information is more like the `python-api-client <https://github.com/meetup/python-api-client>`_.. . The project is located at `github.com/SLCPython/slcpy.com <https://github.com/SLCPython/slcpy.com>`_.. if you want to see the actual implementation. Cheers!

