from django.conf.urls import url, include
from app import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'demographics', views.DemographicsViewSet)
router.register(r'chapters', views.ChapterViewSet)

urlpatterns=[
    url(r'^', include(router.urls)),

    #for creation of events and meetings
    url(r'^events/newEvent/$', views.EventDetailCreate.as_view()),

    #hours updating and checking
    url(r'^hours/check/(?P<pk>[0-9]+)/$', views.check_reqs),
    url(r'^hours/update/(?P<pku>[0-9]+)/(?P<pke>[0-9]+)/(?P<hours>[0-9]+(\.[0-9]))/$', views.add_event),


    #intiate pledges
    url(r'^pledges/initiate/(?P<pk>[0-9]+)/$', views.initiate_pledges),
]
