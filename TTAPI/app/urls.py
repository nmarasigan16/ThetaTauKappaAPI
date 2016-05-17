from django.conf.urls import url, include
from restapi import views
from rest_framework.routers import DefaultRouter

from app.views import(
        LoginView, LogoutView, PasswordChangeView,
        PasswordResetView, PasswordResetConfirmView)

urlpatterns = [
    #non auth urls
    url(r'^password/reset/$', PasswordResetView.asview(),
        name = 'password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^login/$', LoginView.as_view(), name='login'),

    #urls requiring authorization
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^password/change/(?P<pk>/$', PasswordChangeView.as_view(), name='change_password')
]
