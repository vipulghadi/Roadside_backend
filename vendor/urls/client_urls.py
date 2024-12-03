
from django.contrib import admin
from django.urls import path
from vendor.views.client_side import *

urlpatterns = [
    path('vendor-registration/', CreateVendorAccountView.as_view(),name='create-vendor-account'),
    path('get-nearby-vendors/', GetNearbyYouVendorsAPI.as_view(),name='nearby-vendors'),
    path('explore-nearby-vendors/', ExploreNearbyVendorsAPI.as_view(),name='nearby-vendors-explore'),
    path('get-vendors-with-offers/', GetVendorWithOffersAPI.as_view(),name='offers'),
    path('get-vendor-profile/<slug>/', GetVendorProfileAPI.as_view(),name='get-vendors-profile'),
    path('get-vendor-food-items/<slug>/', GetVendorFoodItemsAPI.as_view(),name='get-vendors-food-items'),
    path('get-vendor-ratings/<slug>/', GetVendorRatingsAPI.as_view(),name='get-vendors-food-items'),
    path('vendor-reviews/', VendorReviewsListCreateAPI.as_view(),name='vendor-reviews'),
    path('rate-vendor/', RateVendorAPI.as_view(),name='rate-vendor'),
    path('get-vendor-ratings/<slug>/', GetVendorRatingsAPI.as_view(),name='vendor-ratings'),
    path('get-popular-food-item-vendors/<pk>/', GetPopularFoodItemVendorsList.as_view(),name='get-popular-food-item-vendors-list'),
    path('discover-local-vendors/', DiscoverLocalVendorsAPI.as_view(),name='discover-local-vendors'),
    
    
    path('vendor-profile/', VendorProfileDetailView.as_view(),name='vendor-profile'),
    path('vendor-images/', VendorImagesListCreate.as_view(),name='vendor-images'),
    path('vendor-images/<pk>/', VendorImagesDetail.as_view(),name='vendor-images-detailed'),
    path('food-items/', VendorFoodItemListCreate.as_view(),name='vendor-food-items'),
    path('food-items/<pk>/', VendorFoodItemDetail.as_view(),name='vendor-food-items-detail'),
    
    
    
    
    
    #for testing
    path('add-vendor-images/', AddVendorImages.as_view(),name='d'),
    path('add-vendor-food-items/', BulkAddVendorFoodItemAPI.as_view(),name='d-'),
    path('update-slug/', UpdateSlugAPI.as_view(),name='d'),
    
    
    
    
    
]
