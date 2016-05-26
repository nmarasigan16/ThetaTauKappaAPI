from django.conf.urls import url, include
from app import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.DemographicsViewSet)
router.register(r'chapters', views.ChapterViewSet)

urlpatterns=[
    url(r'^', include(router.urls)),

    #for creation of events and meetings
    url(r'^events/newEvent/$', views.EventDetailCreate.as_view())
]
