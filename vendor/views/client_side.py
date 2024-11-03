from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.db import transaction

from Roadside_backend.utils import custom_response,validate_phone_number
from Roadside_backend.otp import generate_otp,validate_otp
from vendor.serializers import *
from Roadside_backend.pagination import PaginationSize20


class CreateVendorAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()
        
        # Extract necessary fields
        first_name = data.pop('first_name', None)
        last_name = data.pop('last_name', None)
        contact_number = data.get('contact_number', None)
        
        # Basic validation
        if not first_name or not last_name or not contact_number:
            return custom_response(
                success=False,
                message="First name, last name, and contact number are required.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user with contact number already exists
        if User.objects.filter(contact_number=contact_number).exists():
            return custom_response(
                success=False,
                message="User with this contact number already exists.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                # Validate and save the Vendor Profile data before creating the User
                serializer = VendorProfileSerializer(data=data)
                if serializer.is_valid():
                    user = User(
                        first_name=first_name,
                        last_name=last_name,
                        contact_number=contact_number,
                        is_active=False,
                        role="vendor"
                    )
                    user.set_unusable_password() 
                    transaction.on_commit(user.save)
                    serializer.save(user=user)

                    return custom_response(
                        success=True,
                        message="Account created successfully.",
                        status=status.HTTP_201_CREATED
                    )
                else:
                    print(serializer.errors)
                    return custom_response(
                        success=False,
                        errors=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return custom_response(
                success=False,
                message=f"An error occurred: {str(e)}",
            )
            
        
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
        
        