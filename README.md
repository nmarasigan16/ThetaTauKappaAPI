# ThetaTauKappaAPI
An API based off the Django Rest Framework for use in upcoming webapp and mobile apps for the members of the Kappa chapter of Theta Tau

## Endpoints

    /users/ - View all users
    /users/detail/(?P<pk>[0-9]+)/ - View a users details
    /events/ -  View all events
    /events/detail/(?P<pk>[0-9]+)/ - View event details

    #utility functions (mostly workarounds)
    /user/chapter/check/ - check a users chapter
    /user/chapter/change/(?P<pk>[0-9]+)/ - Change a users chapter

    #all user functions
    /hours/check/ - Check a users hours
    /hours/update/(?P<pke>[0-9]+)/(?P<hours>[0-9]+(\.(5|0))?)/ - Add an event to a users hours
    /attendance/update/ - update a users attendance object

    #pledge functions
    /interviews/ - View all interviews owned by user
    /interviews/(?P<pk>[0-9]+)/ - view a specific interview
    /interviews/log/ - submit an interview

    #officer functions
    /pledges/initiate/ - initiate pledges.  Change their status
    /attendance/(?P<pk>[0-9]+)/ - take attendance for a meeting
    /email/(?P<who>(B|P|A))/ -  Email a subset of users
    
    #admin functions
    /user/delete/(?P<pk>[0-9]+)/ - delete a user
    /user/officers/change/(?P<pk>[0-9]+)/(?P<operation>0|1|273)/ - make a user an officer

## Motivation

Simplify and speed up the process of logging and checking hours and attendance
