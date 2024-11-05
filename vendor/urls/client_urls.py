
from django.contrib import admin
from django.urls import path
from vendor.views.client_side import *

urlpatterns = [
    path('vendor-registration/', CreateVendorAccountView.as_view(),name='create-vendor-account'),
    path('vendor-profile/', VendorProfileDetailView.as_view(),name='vendor-profile'),
    path('vendor-images/', VendorImagesListCreate.as_view(),name='vendor-images'),
    path('vendor-images/<pk>/', VendorImagesDetail.as_view(),name='vendor-images-detailed'),
    path('food-items/', VendorFoodItemListCreate.as_view(),name='vendor-food-items'),
    path('food-items/<pk>/', VendorFoodItemDetail.as_view(),name='vendor-food-items-detail'),
    
    
    
    
    
]
