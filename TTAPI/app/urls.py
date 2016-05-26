from django.conf.urls import url, include
from app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.DemographicsViewSet)
router.register(r'chapters', views.ChapterViewSet)

urlpatterns=[
    url(r'^', include(router.urls)),
]
