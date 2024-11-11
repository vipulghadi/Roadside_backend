
from django.contrib import admin
from django.urls import path
from food_items.views.client_side import *

urlpatterns = [
    path('get-top-8-food-item-suggestions/', GetTop8FoodItemsSuggestionsAPI.as_view(),name='food-item-sugestionsl'),
    path('get-top-10-food-item-suggestions/', GetTop10FoodItemsSuggestionsAPI.as_view(),name='food-item-sugestions'),
    path('get-popular-food-items/', GetPopularFoodItemsAPI.as_view(),name='popular-food-items'),
    path('search-by-food-item/', SearchBYFoodItem.as_view(),name='search-by-item'),
    

]