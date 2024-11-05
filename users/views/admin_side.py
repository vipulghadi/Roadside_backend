from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

from Roadside_backend.utils import custom_response,validate_phone_number
from Roadside_backend.otp import generate_otp,validate_otp
from users.serializers import *
from Roadside_backend.pagination import PaginationSize20
from vendor.models import VendorProfile
from vendor.serializers import VendorProfileSerializer

class GetAllUsers(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        return User.objects.all()
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
    
    
class GetAllVendors(ListAPIView):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer
    permission_classes = [AllowAny]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        return VendorProfile.objects.all()
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
