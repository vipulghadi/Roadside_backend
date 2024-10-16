
from django.contrib import admin
from django.urls import path
from food_items.views.admin_side import *

urlpatterns = [
    path('food-item-category/', FoodItemCategoryListCreateView.as_view(),name='food-item-category'),
    path('food-item-category/<pk>/', FoodItemCategoryDetailed.as_view(),name='food-item-category-detail'),
    path('food-item/', FoodItemListCreateView.as_view(),name='food-item'),
    path('food-item/<pk>', FoodItemDetailed.as_view(),name='food-item-detail'),
    
]