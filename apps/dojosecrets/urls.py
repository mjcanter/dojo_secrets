# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^popular$', views.popular),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^secret$', views.secret),
    url(r'delete$', views.delete),
    url(r'like$', views.like),
    url(r'^popsecret$', views.popsecret),
    url(r'popdelete$', views.popdelete),
    url(r'poplike$', views.poplike),
    url(r'deleteuser$', views.deleteuser),
    url(r'^logout$', views.logout),
    ]