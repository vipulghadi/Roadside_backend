
from django.contrib import admin
from django.urls import path
from vendor.views.admin_side import *

urlpatterns = [
    path('vendor-list/', VendorProfileListView.as_view(),name='vendor-profile-list'),
    
]
