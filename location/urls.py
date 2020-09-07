from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',signin,name='signin'),
    path('loginpro/',loginpro,name="loginpro"),
    path('forgot/',forgot,name="forgot"),
    path('send_reset_code/',send_reset_code,name="send_reset_code"),
    path('enter_reset_code/',enter_reset_code,name="enter_reset_code"),
    path('resetpass/',resetpass,name="resetpass"),
    path('resetpasspro/<str:code>/',resetpasspro,name="resetpasspro"),
    path('searchzoom/',searchzoom,name="searchzoom"),
    path('operate_location/',operate_location,name="operate_location"),
]
