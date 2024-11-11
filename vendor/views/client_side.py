from django.shortcuts import render
from  rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.db import transaction
import random
from rest_framework.response import Response


from Roadside_backend.utils import custom_response,validate_phone_number,generate_slug
from Roadside_backend.otp import generate_otp,validate_otp
from vendor.serializers import *
from Roadside_backend.pagination import PaginationSize20
from Roadside_backend.permissions import IsVendor,IsAdmin,IsAdminOrSuperAdmin,IsStaffMember,IsSuperAdmin
from vendor.tasks import send_Vendor_welcome_email
from users.utils import is_valid_contact_number,is_valid_email



#testing addition apis for me
class AddVendorImages(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        links=request.data.get("links")
        vendor_id=request.data.get("vendor_id")
        
        for link in links:
            VendorImages.objects.create(vendor_id=vendor_id,image_link=link)
        
        return custom_response(
            success=True,
            message=f"Vendor images added successfully. for vendor {vendor_id}",
            status=status.HTTP_200_OK)

class BulkAddVendorFoodItemAPI(APIView):
    permission_classes=[AllowAny]
    def post(self, request, *args, **kwargs):
            try:
                # Loop through each vendor in the VendorProfile model
                for vendor in VendorProfile.objects.all():
                    # Get all food items and select 10 random items
                    all_food_items = list(FoodItem.objects.all())
                    random_food_items = random.sample(all_food_items, 10)

                    # Create VendorFoodItem entries for the selected random food items
                    for food_item in random_food_items:
                        VendorFoodItem.objects.create(vendor=vendor, food_item=food_item)

                # Return a success response if everything goes well
                return Response({"message": "Successfully added 10 random food items to each vendor."}, status=status.HTTP_201_CREATED)

            except Exception as e:
                # If any error occurs, catch it and return a failure response with the error message
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UpdateSlugAPI(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        vendor_items=VendorFoodItem.objects.all()
        for item in vendor_items:
        # Generate a random price between 50 and 500
            random_price = round(random.uniform(50, 500), 2)

            # Randomly decide if the item has an offer (50% chance)
            is_offer = random.choice([True, False])

            # Generate a random discount percentage between 5% and 50% if there is an offer
            offer_discount = random.randint(5, 50) if is_offer else 0

            # Calculate the offer price if there is an offer, else keep it as the random price
            offer_price = random_price - (random_price * offer_discount / 100) if is_offer else random_price

            # Update the fields
            item.price = random_price
            item.is_offer = is_offer
            item.offer_discount = offer_discount
            item.offer_price = round(offer_price, 2)

            # Save the changes for the current item
            item.save()

        return custom_response(
            success=True,
            message="Slugs updated successfully for all vendors.",
            status=status.HTTP_200_OK)
        
def get_vendor(request):
    try:
        return VendorProfile.objects.get(owner_id=request.user.id,is_deleted=False)
    except:
        raise Http404("not found")
    
#client side apis
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


class GetNearbyYouVendorsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response_data = []
        try:
            nearby_vendors = VendorProfile.objects.all()[:15]
            
            for vendor in nearby_vendors:
                food_items = VendorFoodItem.objects.filter(vendor=vendor, is_deleted=False)[:2]
                vendor_image = VendorImages.objects.filter(vendor=vendor, is_deleted=False).first()
                vendor_food_items_serializer = VendorFoodItemsSerializer(food_items, many=True)
                
                response_data.append({
                    "id":vendor.id,
                    "vendor_profile": {
                        "vendor_name":vendor.vendor_name,
                        "owner":vendor.owner.first_name+vendor.owner.last_name,
                         "rating":vendor.rating,
                         "logitude":vendor.longitude,
                         "latitude":vendor.latitude,
                         "slug":vendor.slug
                },
                    "vendor_image": vendor_image.image_link,
                    "food_items": vendor_food_items_serializer.data
                })
            
            # Return response after processing all vendors
            return custom_response(
                success=True,
                data=response_data,
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print(e)
            return custom_response(
                success=False,
                message="An error occurred while fetching nearby vendors.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
            
class GetVendorWithOffersAPI(APIView):
    permission_classes=[AllowAny]
    def get(self, request, *args, **kwargs):
        response_data = []

        try:
            nearby_vendors = VendorProfile.objects.filter(is_deleted=False,is_offer=True)[:10]
            
            for vendor in nearby_vendors:
                food_items = VendorFoodItem.objects.filter(vendor=vendor, is_deleted=False)[:2]
                vendor_image = VendorImages.objects.filter(vendor=vendor, is_deleted=False).first()
                vendor_food_items_serializer = VendorFoodItemsSerializer(food_items, many=True)
            
                response_data.append({
                    "id":vendor.id,
                    "vendor_profile": {
                        "vendor_name":vendor.vendor_name,
                        "owner":vendor.owner.first_name+vendor.owner.last_name,
                         "rating":vendor.rating,
                         "logitude":vendor.longitude,
                         "latitude":vendor.latitude,
                         "maximum_discount":vendor.maximum_discount,
                         "slug":vendor.slug
                },
                    "vendor_image":  vendor_image.image_link or "",
                    "food_items": vendor_food_items_serializer.data
                })
            
            # Return response after processing all vendors
            return custom_response(
                success=True,
                data=response_data,
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print(e)
            return custom_response(
                success=False,
                message="An error occurred while fetching nearby vendors.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
        
class GetVendorProfileAPI(APIView):
    permission_classes=[AllowAny]
    def get_object(self,slug):
        try:
            return VendorProfile.objects.get(slug=slug, is_deleted=False)
        except VendorProfile.DoesNotExist:
            raise Http404("not found")
    def get(self, request, slug,*args, **kwargs):
        inst = self.get_object(slug)
        vendor_images=VendorImages.objects.filter(vendor=inst,is_deleted=False)[:3]
        vendor_image_serializer=VendorImagesSerializer(vendor_images,many=True)
        serializer = VendorProfileSerializer(inst)
        return custom_response(
            success=True,
            data={
                "vendor_profile":serializer.data,
                "vendor_images":vendor_image_serializer.data
            },
            status=status.HTTP_200_OK
        )

class GetVendorFoodItemsAPI(APIView):
    permission_classes=[AllowAny]
    
    def get_object(self, slug):
        try:
            return VendorProfile.objects.get(slug=slug, is_deleted=False)
        except VendorProfile.DoesNotExist:
            raise Http404("not found")
        
    def get(self, request, slug):
        vendor = self.get_object(slug)
        food_items = VendorFoodItem.objects.filter(vendor=vendor, is_deleted=False)
        serializer = VendorFoodItemsSerializer(food_items, many=True)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
        
class GetVendorRatingsAPI(APIView):
    permission_classes=[AllowAny]
    def get_object(self,slug):
        try:
            return VendorProfile.objects.get(slug=slug, is_deleted=False)
        except VendorProfile.DoesNotExist:
            raise Http404("not found")
    def get(self, request, slug):
        vendor = self.get_object(slug)
        ratings = VendorRating.objects.filter(vendor=vendor, is_deleted=False)
        serializer = VendorRatingSerializer(ratings, many=True)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )    
# class GetVendorReviewsAPI(APIView):
#     permission_classes=[AllowAny]
    
#     def get_object(self, pk):
#         try:
#             return VendorProfile.objects.get(pk=pk, is_deleted=False)
#         except VendorProfile.DoesNotExist:
#             raise Http404("not found")
        
#     def get(self.request,pk):
#         vendor = self.get_object(pk)
#         reviews = VendorReview.objects.filter(vendor=vendor, is_deleted=False)
#         serializer = ReviewSerializer(reviews, many=True)
#         return custom_response(
#             success=True,
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
            
class VendorReviewsListCreateAPI(APIView):
    permission_classes=[AllowAny]
    def get_object(self, slug):
        ...
    def post(self, request):
        data=request.data
        serializer = VendorReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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
        
        
        
        
        
        

#vendor-side crud        
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


        