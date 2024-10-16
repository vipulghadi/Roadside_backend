from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from django.http import Http404


from Roadside_backend.utils import custom_response,validate_phone_number
from Roadside_backend.otp import generate_otp,validate_otp
from users.serializers import *
from Roadside_backend.pagination import PaginationSize20
from Roadside_backend.permissions import IsAuthenticatedAndActive

# Create your views here.
class UserListView(ListAPIView):
    serializer_class =UserSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    permission_classes=[AllowAny]

    def get_queryset(self):
        queryset =  User.objects.filter(is_deleted=False).order_by('-id')
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

class UserDetailed(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk, is_deleted=False)
        except User.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = UserSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = UserSerializer(inst, data=request.data)
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
        inst = self.get_object(pk)
        inst.is_deleted = True
        inst.save()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )

class UserProfileCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=self.request.user.id)
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return custom_response(
            success=False,
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserProfileDetail(APIView):
    def get_object(self,pk):
        try:
            return UserProfile.objects.get(pk=pk, user_id=self.request.user.id)
        except UserProfile.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = UserProfileSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, format=None):
        inst= self.get_object(pk)
        serializer = UserProfileSerializer(inst, data=request.data)
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
        inst = self.get_object(pk)
        inst.delete()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )
