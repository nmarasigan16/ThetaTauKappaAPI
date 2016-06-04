from django.conf.urls import url, include
from app import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#Officer only urls
router.register(r'events/full', views.EventViewSet)
router.register(r'meetings/full', views.MeetingViewSet)
#admin only urls
router.register(r'demographics/full', views.DemographicsViewSet)
router.register(r'chapters/full', views.ChapterViewSet)
router.register(r'users/full', views.UserViewSet)

urlpatterns=[
    url(r'^', include(router.urls)),

    url(r'^users/$', views.UserDetailList.as_view()),
    url(r'^events/$', views.EventDetailList.as_view()),

    #utility functions (mostly workarounds)
    url(r'^user/chapter/check/$', views.has_chapter),
    url(r'^user/chapter/change/(?P<pk>[0-9]+)/$', views.change_chapter),

    #all user functions
    url(r'^hours/check/(?P<pk>[0-9]+)/$', views.check_reqs),
    url(r'^hours/update/(?P<pke>[0-9]+)/(?P<hours>(?:[1-9]\d*|0)?(?:\.5*)?)/$', views.add_event),
    url(r'^attendance/update/$', views.AttendanceDetail.as_view()),

    #officer functions
    url(r'^pledges/initiate/(?P<pk>[0-9]+)/$', views.initiate_pledges),

    #admin functions
    url(r'^user/delete/(?P<pk>[0-9]+)/$', views.delete_user),
    url(r'^user/officers/change/(?P<pk>[0-9]+)/(?P<operation>0|1|273)/$', views.modify_officer_status),

]
