Django-Meetup
=============

This is a general purpose django-app for syncing with Meetup.com and adding adding Meetup.com content to your website.

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
    
    # **Security Warning:** Keep personal Meetup api key secret, read `Meetup documentation <https://secure.meetup.com/meetup_api/key/>`_.
    
    MEETUP_ALLOW_ADMIN = True

    # (optional) This boolean will set up admin interface. 
    # **WARNING:** Methods to sync TO Meetup have not been completed. So any changes to the database are local.
    
    MEETUP_GROUP_ID = 123456789

    # (optional) This is the default group id to get information from


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

