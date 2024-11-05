from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import Http404

from Roadside_backend.pagination import PaginationSize20
from Roadside_backend.utils import custom_response
from food_items.serializers import *
from food_items.models import *

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
