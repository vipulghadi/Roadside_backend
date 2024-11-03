from django.contrib import admin
from django.urls import path
from authentication.views.client_side import *

urlpatterns = [
    path('otp-login/', OTPLoginView.as_view(),name='otp-login'),
    path('get-current-user/', GetCurrentUser.as_view(),name='get-current-user'),
    
]