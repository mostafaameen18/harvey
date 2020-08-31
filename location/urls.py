from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',redirector),
    path('searchzoom/',searchzoom,name="searchzoom"),
    path('operate_location/',operate_location,name="operate_location"),
]
