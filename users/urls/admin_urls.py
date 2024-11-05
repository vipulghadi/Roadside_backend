
from django.contrib import admin
from django.urls import path
from users.views.admin_side import *

urlpatterns = [
    path('get-all-users/', GetAllUsers.as_view(),name='get-all-users'),
    path('get-all-vendors/', GetAllVendors.as_view(),name='get-all-vendors'),
    
]