from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.core.cache import cache

from Roadside_backend.pagination import PaginationSize20
from Roadside_backend.utils import custom_response
from food_items.serializers import *
from food_items.models import *
from vendor.models import VendorProfile,VendorFoodItem,VendorImages

class GetTop8FoodItemsSuggestionsAPI(APIView):
    
    def get(self, request):
        query = request.query_params.get("query", "")
        
        if query:
            food_items = FoodItem.objects.filter(name__icontains=query)[:8]
            serializer = FoodItemSerializer(food_items, many=True)
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return custom_response(
                success=True,
                data=[],
                status=status.HTTP_200_OK
            )

class GetTop10FoodItemsSuggestionsAPI(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        query = request.query_params.get("query", "")
        
        if query:
            food_items = FoodItem.objects.filter(name__icontains=query)[:8]
            serializer = FoodItemSerializer(food_items, many=True)
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return custom_response(
                success=True,
                data=[],
                status=status.HTTP_200_OK
            )

class GetPopularFoodItemsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Define the cache key
        cache_key = 'popular_food_items'

        # Try to get data from Redis cache
        cached_food_items = cache.get(cache_key)

        if cached_food_items:
            # If data is found in the cache, return it
            return custom_response(
                success=True,
                data=cached_food_items,
                status=status.HTTP_200_OK
            )

        # If not in cache, query the database
        food_items = FoodItem.objects.filter(is_deleted=False)[:15]

        # Serialize the food items
        serializer = FoodItemSerializer(food_items, many=True)

        # Cache the food items for 1 hour (3600 seconds)
        cache.set(cache_key, serializer.data, timeout=3600)

        # Return the data in the response
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
        
class SearchBYFoodItem(APIView):
    permission_classes=[AllowAny]
    
    def get(self, request, *args, **kwargs):
        food_item_id = request.query_params.get('food_item_id')
        if not food_item_id:
            return custom_response(
                success=False,
                message="Food item ID is required.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        food_item=FoodItem.objects.get(id=food_item_id)
        
        try:
        
            vendor_food_items=VendorFoodItem.objects.filter(food_item=food_item,is_deleted=False)
            response=[]
            print(vendor_food_items.count())
            for vendor_food_item in vendor_food_items:
                vendor=VendorProfile.objects.filter(id=vendor_food_item.vendor.id).first()
                vendor_image=VendorImages.objects.filter(vendor=vendor).first()
                response.append(
                    {
                        "vendor_name":vendor.vendor_name,
                        "contact_number":vendor.contact_number,
                        "address":vendor.address,
                        "rating":vendor.rating,
                        "is_offer":vendor.is_offer,
                        "maximum_discount":vendor.maximum_discount,
                        "food_type":vendor.food_type,
                        "longitude":vendor.longitude,
                        "sitting_available":vendor.sitting_available,
                        "latitude":vendor.latitude,
                        "vendor_image":vendor_image.image_link
                    }
                
    
                )
            
            return custom_response(
                success=True,
                data=response,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return custom_response(
                success=False,
                message="An error occurred while searching for food item.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
    
