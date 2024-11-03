
from django.contrib import admin
from django.urls import path
from vendor.views.client_side import *

urlpatterns = [
    path('vendor-registration/', CreateVendorAccountView.as_view(),name='create-vendor-account'),
    
]
