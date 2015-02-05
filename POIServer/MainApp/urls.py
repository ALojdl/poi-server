from django.conf.urls import patterns, url

from MainApp import views

urlpatterns = patterns('',
   url(r'^poireport', views.report, name='report'),
   url(r'^storecategories', views.get_categories, name='getcategories'),
   url(r'^fourservice', views.foursquare_service, name='fourservice'),
   url(r'^testing', views.testing, name='testing'),
)