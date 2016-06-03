from django.conf.urls import url, include
from app import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'demographics', views.DemographicsViewSet)
router.register(r'chapters', views.ChapterViewSet)
router.register(r'events/edit', views.EventViewSet)

urlpatterns=[
    url(r'^', include(router.urls)),

    #utility functions (mostly workarounds)
    url(r'^user/chapter/check/$', views.has_chapter),
    url(r'^user/chapter/change/(?P<pk>[0-9]+)/$', views.change_chapter),

    #all user functions
    url(r'^hours/check/(?P<pk>[0-9]+)/$', views.check_reqs),
    url(r'^hours/update/(?P<pku>[0-9]+)/(?P<pke>[0-9]+)/(?P<hours>[0-9]+(\.[0-9]))/$', views.add_event),

    #officer functions
    url(r'^pledges/initiate/(?P<pk>[0-9]+)/$', views.initiate_pledges),
    #for events
    url(r'^events/add/$', views.EventDetailCreate.as_view()),
    url(r'^events/update/$', views.EventDetailUpdate.as_view()),
    #for meetings
    url(r'^meetings/add/$', views.MeetingDetailCreate.as_view()),
    url(r'^meetings/update/$', views.MeetingDetailUpdate.as_view()),

    #admin functions
    url(r'^user/delete/(?P<pk>[0-9]+)/$', views.delete_user),
    url(r'^user/officers/change/(?P<pk>[0-9]+)/(?P<operation>0|1|273)/$', views.modify_officer_status),

]
