'''
Created on Nov 21, 2015

@author: nwilliams
'''

from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index')
]