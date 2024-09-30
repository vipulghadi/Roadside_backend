from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.permissions import AllowAny
from django.http import Http404

from SeeMe_be.utils import custom_response,validate_phone_number
from SeeMe_be.otp import generate_otp,validate_otp
from vendor.serializers import *
from SeeMe_be.pagination import PaginationSize20


class VendorProfileCreateView(APIView):
    def post(self, request, format=None):
        request.data._mutable = True  
        serializer = VendorProfileSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=data,
                    status=status.HTTP_201_CREATED
                )
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class VendorProfileDetailView(APIView):
    def get_object(self, pk):
        try:
            return VendorProfile.objects.get(pk=pk, is_deleted=False)
        except VendorProfile.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorProfileSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorProfileSerializer(inst, data=request.data)
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

    def delete(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        inst.is_deleted = True
        inst.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )


class VendorImagesListCreate(ListAPIView):
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        user=self.request.user
        queryset = VendorImages.objects.filter(vendor__owner=user)
    
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
                    data=self.get_paginated_response(serializer.data),
                    status=status.HTTP_200_OK
                )
    
    def post(self, request, format=None):
        serializer = VendorImagesSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=data,
                    status=status.HTTP_201_CREATED
                )
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class VendorImagesDetail(APIView):
    def get_object(self, pk):
        try:
            return VendorImages.objects.get(pk=pk, is_deleted=False)
        except VendorImages.DoesNotExist:
            raise Http404("not found")
            
    
    def get(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorImagesSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorImagesSerializer(inst, data=request.data)
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
    
    def delete(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        inst.is_deleted = True
        inst.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )
    
class VendorFoodItemListCreate(ListAPIView):
    
    def get_queryset(self):
        user=self.request.user
        queryset = VendorFoodItem.objects.filter(vendor__owner=user)
    
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
                    data=self.get_paginated_response(serializer.data),
                    status=status.HTTP_200_OK
                )
    
    def post(self, request, format=None):
        serializer = VendorFoodItemsSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=data,
                    status=status.HTTP_201_CREATED
                )
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class VendorFoodItemDetail(APIView):
    def get_object(self, pk):
        try:
            return VendorFoodItem.objects.get(pk=pk, is_deleted=False)
        except VendorFoodItem.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorFoodItemsSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorFoodItemsSerializer(inst, data=request.data)
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
    
    def delete(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        inst.is_deleted = True
        inst.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )

class VendorFoodItemImagesListCreate(ListAPIView):
    pagination_class = PaginationSize20
    serializer_class=VendorFoodItemImagesSerializer
    
    def get_queryset(self):
        user=self.request.user
        queryset = VendorFoodItemImage.objects.filter(vendor_food_item__vendor__owner=user)
    
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
                    data=self.get_paginated_response(serializer.data),
                    status=status.HTTP_200_OK
                )
    
    def post(self, request, format=None):
        serializer = VendorFoodItemImagesSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=data,
                    status=status.HTTP_201_CREATED
                )
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class VendorFoodItemImagesDetail(APIView):
    def get_object(self, pk):
        try:
            return VendorFoodItemImage.objects.get(pk=pk, is_deleted=False)
        except VendorFoodItemImage.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorFoodItemImagesSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorFoodItemImagesSerializer(inst, data=request.data)
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
    
    def delete(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        inst.is_deleted = True
        inst.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )

class VendorLikesListCreate(ListAPIView):
    pagination_class = PaginationSize20
    serializer_class=VendorLikesSerializer
    
    def get_queryset(self):
        user=self.request.user
        queryset = VendorLikes.objects.filter(vendor__owner=user)
    
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
                    data=self.get_paginated_response(serializer.data),
                    status=status.HTTP_200_OK
                )
    
    def post(self, request, format=None):
        serializer = VendorLikesSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=data,
                    status=status.HTTP_201_CREATED
                )
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class VendorLikesDetail(APIView):
    def get_object(self, pk):
        try:
            return VendorLikes.objects.get(pk=pk, is_deleted=False)
        except VendorLikes.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorLikesSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        serializer = VendorLikesSerializer(inst, data=request.data)
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
    
    def delete(self, request, pk, *args, **kwargs):
        inst = self.get_object(pk)
        inst.is_deleted = True
        inst.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )
        
        