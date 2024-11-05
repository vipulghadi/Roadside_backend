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
from Roadside_backend.permissions import IsVendor,IsAdmin,IsAdminOrSuperAdmin,IsStaffMember,IsSuperAdmin
from vendor.tasks import send_Vendor_welcome_email
from users.utils import is_valid_contact_number,is_valid_email

#utility function to get vendor
def get_vendor(request):
    try:
        return VendorProfile.objects.get(owner_id=request.user.id,is_deleted=False)
    except:
        raise Http404("not found")
    
class CreateVendorAccountView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        data = request.data.copy()
        
        first_name = data.pop('first_name', None)
        last_name = data.pop('last_name', None)
        contact_number = data.get('contact_number', None)

    
        if not first_name or not last_name or not contact_number:
            return custom_response(
                success=False,
                message="First name, last name, and contact number are required.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not is_valid_contact_number(contact_number):
            return custom_response(
                success=False,
                message="Invalid contact number format.",
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
                    user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        contact_number=contact_number,
                        is_active=True,
                        role="vendor"
                    )
                    user.set_unusable_password() 
                    user.save()
                    serializer.save(owner=user)
                    #send_Vendor_welcome_email.delay("vipulvijayghadi@gmail.com", first_name, last_name)
            
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
            print(e)
            return custom_response(
                success=False,
                message=f"An error occurred:",
            )
            
class VendorProfileDetailView(APIView):
    permission_classes = [IsVendor |IsAdminOrSuperAdmin|IsStaffMember]
    def get_object(self, user):
        try:
            return VendorProfile.objects.get(owner=user, is_deleted=False)
        except VendorProfile.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, *args, **kwargs):
        inst = self.get_object(user=request.user)
        serializer = VendorProfileSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        inst = self.get_object(user=request.user)
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


class VendorImagesListCreate(ListAPIView):
    permission_classes = [IsVendor | IsAdminOrSuperAdmin | IsStaffMember]
    serializer_class = VendorImagesSerializer
    pagination_class=PaginationSize20

    def get_queryset(self):
        user = self.request.user
        queryset= VendorImages.objects.filter(vendor__owner=user,is_deleted=False)
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
                    data=self.get_paginated_response(serializer.data).data, 
                    status=status.HTTP_200_OK
                )
        
        serializer = self.get_serializer(queryset, many=True)
        return custom_response(
            success=True,
            data=serializer.data, 
            status=status.HTTP_200_OK
        )

    

    def post(self, request, format=None):
        vendor = get_vendor(request)
        request_data = request.data.copy()
        request_data["vendor"] = vendor.id
    
        serializer = VendorImagesSerializer(data=request_data)
        if serializer.is_valid():
            data = serializer.save()
            return custom_response(
                success=True,
                data=VendorImagesSerializer(data).data,
                status=status.HTTP_201_CREATED
            )
        return custom_response(
            success=False,
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    
class VendorImagesDetail(APIView):
    permission_classes = [IsVendor |IsAdminOrSuperAdmin|IsStaffMember]
    def get_object(self, pk):
        try:
            return VendorImages.objects.get(pk=pk, is_deleted=False,vendor__owner=self.request.user)
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
    permission_classes = [IsVendor |IsAdminOrSuperAdmin|IsStaffMember]
    serializer_class=VendorFoodItemsSerializer
    pagination_class=PaginationSize20
    def get_queryset(self):
        user=self.request.user
        queryset = VendorFoodItem.objects.filter(vendor__owner=user,is_deleted=False)
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
                    data=self.get_paginated_response(serializer.data).data, 
                    status=status.HTTP_200_OK
                )
        
        # Return non-paginated response if no page param is present
        serializer = self.get_serializer(queryset, many=True)
        return custom_response(
            success=True,
            data=serializer.data,  # Directly serialize the full queryset
            status=status.HTTP_200_OK
        )
    def post(self, request, format=None):
        vendor=get_vendor(request)
        request_data=request.data.copy()
        request_data["vendor"]=vendor.id
    
        serializer = VendorFoodItemsSerializer(data=request_data)
        if serializer.is_valid():
            data=serializer.save()
            return custom_response(
                    success=True,
                    data=VendorFoodItemsSerializer(data).data,
                    status=status.HTTP_201_CREATED
                )
        print(serializer.errors)
        return custom_response(
                    success=False,
                    errors=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class VendorFoodItemDetail(APIView):
    permission_classes = [IsVendor |IsAdminOrSuperAdmin|IsStaffMember]
    def get_object(self, request,pk):
        try:
            return VendorFoodItem.objects.get(pk=pk, is_deleted=False,vendor__owner=request.user)
        except VendorFoodItem.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, *args, **kwargs):
        inst = self.get_object(request,pk)
        serializer = VendorFoodItemsSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    # def put(self, request, pk, *args, **kwargs):
    #     inst = self.get_object(pk)
    #     serializer = VendorFoodItemsSerializer(inst, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return custom_response(
    #             success=True,
    #             data=serializer.data,
    #             status=status.HTTP_200_OK
    #         )
    #     return custom_response(
    #         success=False,
    #         errors=serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
    
    def delete(self, request, pk, *args, **kwargs):
        inst = self.get_object(request,pk)
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
        
        