
from django.contrib import admin
from django.urls import path
from users.views.client_side import *

urlpatterns = [
    path('otp-signup/', OTPSignupView.as_view(),name='otp-signup'),
    path('otp-login/', OTPLoginView.as_view(),name='otp-login'),
    
]