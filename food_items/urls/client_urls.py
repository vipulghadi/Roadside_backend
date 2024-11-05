
from django.contrib import admin
from django.urls import path
from food_items.views.client_side import *

urlpatterns = [
    path('get-top-8-food-item-suggestions/', GetTop8FoodItemsSuggestionsAPI.as_view(),name='food-item-sugestionsl'),
    

]