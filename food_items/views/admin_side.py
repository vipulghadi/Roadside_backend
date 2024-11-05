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

class FoodItemCategoryListCreateView(ListAPIView):
    serializer_class =FoodItemCategorySerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    permission_classes=[AllowAny]

    def get_queryset(self):
        queryset =  ItemCategory.objects.filter(is_deleted=False).order_by('-id')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_param = self.request.query_params.get("page")
        if page_param:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return custom_response(
                    success=True,
                    data=self.get_paginated_response(serializer.data),
                    status=status.HTTP_200_OK
                )
                
        serializer = self.get_serializer(queryset, many=True)
        return  custom_response(
                    success=True,
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
    
    def post(self, request, format=None):
        data=request.data
        serializer = FoodItemCategorySerializer(data=data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=FoodItemCategorySerializer(data).data,
                    status=status.HTTP_201_CREATED
                )
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class FoodItemCategoryDetailed(APIView):
    def get_object(self,pk):
        try:
            return ItemCategory.objects.get(pk=pk, is_deleted=False)
        except ItemCategory.DoesNotExist:
            raise Http404("not found")
            
            
    
    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = FoodItemCategorySerializer(item)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = FoodItemCategorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return custom_response(
            success=False,
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.is_deleted = True
        item.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )

class FoodItemListCreateView(ListAPIView):
    serializer_class = FoodItemSerializer
    renderer_classes = [JSONRenderer]
    permission_classes=[AllowAny]
    
    
    def get_queryset(self):
        queryset = FoodItem.objects.filter(is_deleted=False).order_by('-id')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_param = self.request.query_params.get("page")
        if page_param:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return custom_response(
                    success=True,
                    data=self.get_paginated_response(serializer.data),
                    status=status.HTTP_200_OK
                )
                
        serializer = self.get_serializer(queryset, many=True)
        return  custom_response(
                    success=True,
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=FoodItemSerializer(data).data,
                    status=status.HTTP_201_CREATED
                )
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
    
class FoodItemDetailed(APIView):
    def get_object(self,pk):
        try:
            return FoodItem.objects.get(pk=pk, is_deleted=False)
        except FoodItem.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = FoodItemSerializer(item)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = FoodItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return custom_response(
                success=False,
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.is_deleted = True
        item.save()
        return custom_response(
            success=True,
            data=None,
            message="delted object",
            status=status.HTTP_204_NO_CONTENT
        )
    
    
