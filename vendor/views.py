from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.permissions import AllowAny



from SeeMe_be.utils import custom_response,validate_phone_number
from SeeMe_be.otp import generate_otp,validate_otp
from .serializers import *
from SeeMe_be.pagination import PaginationSize20


class VendorProfileListCreateView(ListAPIView):
    serializer_class = VendorProfileSerializer
    pagination_class = PaginationSize20
      
    def get_queryset(self):
        return  VendorProfile.objects.filter(is_deleted=False).order_by('-id')
    
    
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
        request.data._mutable = True  
        serializer = self.get_serializer(data=request.data)
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
            return custom_response(
                success=False,
                errors={"item": "profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def get(self, request, pk, *args, **kwargs):
        vendor_profile = self.get_object(pk)
        serializer = VendorProfileSerializer(vendor_profile)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        vendor_profile = self.get_object(pk)
        serializer = VendorProfileSerializer(vendor_profile, data=request.data)
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
        vendor_profile = self.get_object(pk)
        vendor_profile.is_deleted = True
        vendor_profile.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )