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
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
                
                
                response_data.append({
                        "id":vendor.id,
                        "vendor_name":vendor.vendor_name,
                        "owner":vendor.owner.first_name+vendor.owner.last_name,
                         "rating":vendor.rating,
                         "logitude":vendor.longitude,
                         "latitude":vendor.latitude,
                         "slug":vendor.slug,
                         "rating":vendor.rating,
                         "address":vendor.address,
                         "food_type":vendor.food_type,
                         "sitting_available":vendor.sitting_available,
                         "is_offer":vendor.is_offer,
                         "maximum_discount":vendor.maximum_discount,
                         "vendor_image": vendor_image.image_link,
                          "location_type": vendor.location_type,
                         "size": vendor.size,
                        
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
    
class ExploreNearbyVendorsAPI(APIView):
    permission_classes = [AllowAny]
    filter_backends =[DjangoFilterBackend,filters.SearchFilter]
    filterset_fields ={
        "open_at":["exact","gte","lte"],
        "close_at":["exact","gte","lte"],
        "food_type":["exact","icontains"],
        "location_type":["exact"],
        "sitting_available":["exact"],
        "size":["exact"],
        
        
    }
    
    
    def get(self, request, *args, **kwargs):
        response_data = []
        try:
            queryset = VendorProfile.objects.all(is_deleted=False)
            paginator=PaginationSize20()
            paginated_queryset=paginator.paginate_queryset(queryset,request)
            
            
            for vendor in paginated_queryset:
                food_items = VendorFoodItem.objects.filter(vendor=vendor, is_deleted=False)[:2]
                vendor_image = VendorImages.objects.filter(vendor=vendor, is_deleted=False).first()
                vendor_food_items_serializer = VendorFoodItemsSerializer(food_items, many=True)
                
                response_data.append({
                        "id":vendor.id,
                        "vendor_name":vendor.vendor_name,
                        "owner":vendor.owner.first_name+vendor.owner.last_name,
                         "rating":vendor.rating,
                         "logitude":vendor.longitude,
                         "latitude":vendor.latitude,
                         "slug":vendor.slug,
                         "rating":vendor.rating,
                         "address":vendor.address,
                         "food_type":vendor.food_type,
                         "sitting_available":vendor.sitting_available,
                         "is_offer":vendor.is_offer,
                         "maximum_discount":vendor.maximum_discount,
                         "vendor_image": vendor_image.image_link,
                         "location_type": vendor.location_type,
                         "size": vendor.size,
                        
                })
            
            paginated_response = paginator.get_paginated_response(response_data)
            # Return response after processing all vendors
            return custom_response(
                success=True,
                data=response_data,
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print(e)
            return custom_response(
                data=[],
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
                        "vendor_name":vendor.vendor_name,
                        "owner":vendor.owner.first_name+vendor.owner.last_name,
                         "rating":vendor.rating,
                         "logitude":vendor.longitude,
                         "latitude":vendor.latitude,
                         "slug":vendor.slug,
                         "rating":vendor.rating,
                         "address":vendor.address,
                         "food_type":vendor.food_type,
                         "sitting_available":vendor.sitting_available,
                         "is_offer":vendor.is_offer,
                         "maximum_discount":vendor.maximum_discount,
                         "vendor_image": vendor_image.image_link,
                          "location_type": vendor.location_type,
                         "size": vendor.size,
                        
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
        
class GetVendorsByFoodItem(APIView):
    permission_classes=[AllowAny]
    
    def get(self, request, *args, **kwargs):
        food_item_id = kwargs.get('food_item_id')
        food_item = FoodItem.objects.filter(id=food_item_id,is_deleted=False).first()
        if not food_item:
            return custom_response(
                success=False,
                message="Food item not found.",
                status=status.HTTP_404_NOT_FOUND
            )
        
        vendors = VendorFoodItem.objects.filter(
                            food_item=food_item, is_deleted=False).values_list('vendor', flat=True)
            
class GetPopularFoodItemVendorsList(APIView):
    permission_classes=[AllowAny]
    def get_object(self, pk):
        try:
            return FoodItem.objects.get(pk=pk,is_deleted=False)  
        except:
            raise Http404("Item not found")  
    
    def get(self,request,pk):
        try:
            food_item = self.get_object(pk)
            response_data=[]
            
            vendors=VendorProfile.objects.filter(is_deleted=False)
            
            #Note :add logic here
            # vendor_ids = VendorFoodItem.objects.filter(food_item=food_item, is_deleted=False).distinct().values_list("id",flat=True)
            # vendors=VendorProfile.objects.filter(id__in=vendor_ids,is_deleted=False).distinct()
            
            paginator=PaginationSize20()
            paginated_queryset=paginator.paginate_queryset(vendors,request)
            
            for vendor in paginated_queryset:
                
                food_items = VendorFoodItem.objects.filter(vendor=vendor, is_deleted=False)[:2]
                vendor_image = VendorImages.objects.filter(vendor=vendor, is_deleted=False).first()
                vendor_food_items_serializer = VendorFoodItemsSerializer(food_items, many=True)
                
                response_data.append({
                            "id":vendor.id,
                            "vendor_name":vendor.vendor_name,
                            "owner":vendor.owner.first_name+vendor.owner.last_name,
                            "rating":vendor.rating,
                            "logitude":vendor.longitude,
                            "latitude":vendor.latitude,
                            "slug":vendor.slug,
                            "rating":vendor.rating,
                            "address":vendor.address,
                            "food_type":vendor.food_type,
                            "sitting_available":vendor.sitting_available,
                            "is_offer":vendor.is_offer,
                            "maximum_discount":vendor.maximum_discount,
                            "vendor_image": vendor_image.image_link,
                            "location_type": vendor.location_type,
                            "size": vendor.size,
                            
                    })
                
            paginated_response=paginator.get_paginated_response(response_data)
            return custom_response(
                success=True,
                data=paginated_response,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return custom_response(
                success=False,
                message="An error occurred while fetching vendor reviews.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class DiscoverLocalVendorsAPI(ListAPIView):
    permission_classes=[AllowAny]
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]
    filterset_fields={
        "is_offer":["exact"],
        "food_type":["exact"],
        "location_type":["exact"],
        "size":["exact"],
        "rating":["gte", "lte"],
        "maximum_discount":["gte", "lte"],
        "sitting_available":["exact"],
    }
    
    
    def get(self, request, *args, **kwargs):
        try:
            response_data=[]
            paginator=PaginationSize20()
            queryset=VendorProfile.objects.filter(is_deleted=False)
            queryset = self.filter_queryset(queryset)
            paginated_queryset=paginator.paginate_queryset(queryset,request)
            
            for vendor in paginated_queryset:
                food_items = VendorFoodItem.objects.filter(vendor=vendor, is_deleted=False)[:2]
                vendor_image = VendorImages.objects.filter(vendor=vendor, is_deleted=False).first()
                vendor_food_items_serializer = VendorFoodItemsSerializer(food_items, many=True)
                
                response_data.append({
                            "id":vendor.id,
                            "vendor_name":vendor.vendor_name,
                            "owner":vendor.owner.first_name+vendor.owner.last_name,
                            "rating":vendor.rating,
                            "logitude":vendor.longitude,
                            "latitude":vendor.latitude,
                            "slug":vendor.slug,
                            "rating":vendor.rating,
                            "address":vendor.address,
                            "food_type":vendor.food_type,
                            "sitting_available":vendor.sitting_available,
                            "is_offer":vendor.is_offer,
                            "maximum_discount":vendor.maximum_discount,
                            "vendor_image": vendor_image.image_link,
                            "location_type": vendor.location_type,
                            "size": vendor.size,
                            
                    })
                    
            paginated_response=paginator.get_paginated_response(response_data)
            return custom_response(
                success=True,
                data=paginated_response,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return custom_response(
                success=False,
                data=None,
                status=status.HTTP_400_BAD_REQUEST
                
            )
        
    
            
            
        
        
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
    
        
class RateVendorAPI(APIView):
    def post(self, request):
        data=request.data
        serializer = VendorRatingSerializer(data=data)
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

class GetVendorRatingsAPI(APIView):
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return VendorProfile.objects.get(slug=slug, is_deleted=False)
        except VendorProfile.DoesNotExist:
            raise Http404("not found")

    def get(self, request, slug):
        try:
            vendor = self.get_object(slug)
            ratings = VendorRating.objects.filter(vendor=vendor, is_deleted=False)

            response = {}
            rating_data={}
            
            total_ratings = ratings.count()
            response["rating_count"] = total_ratings
            
            # Initialize sum and count for each rating category
            behavior_ratings = 0
            service_ratings = 0
            quality_ratings = 0
            cleanliness_ratings = 0
            value_for_money_ratings = 0

            total_behavior = 0
            total_service = 0
            total_quality = 0
            total_cleanliness = 0
            total_value_for_money = 0

            # Calculate sum and count for each rating
            for rating in ratings:
                if rating.behavior_rating:
                    behavior_ratings += rating.behavior_rating
                    total_behavior += 1
                if rating.service_rating:
                    service_ratings += rating.service_rating
                    total_service += 1
                if rating.quality_rating:
                    quality_ratings += rating.quality_rating
                    total_quality += 1
                if rating.cleanliness_rating:
                    cleanliness_ratings += rating.cleanliness_rating
                    total_cleanliness += 1
                if rating.value_for_money_rating:
                    value_for_money_ratings += rating.value_for_money_rating
                    total_value_for_money += 1

            # Calculate average ratings for each category
            rating_data["average_behavior_rating"] = round(
                behavior_ratings / total_behavior, 1) if total_behavior > 0 else 0
            rating_data["average_service_rating"] = round(
                service_ratings / total_service, 1) if total_service > 0 else 0
            rating_data["average_quality_rating"] = round(
                quality_ratings / total_quality, 1) if total_quality > 0 else 0
            rating_data["average_cleanliness_rating"] = round(
                cleanliness_ratings / total_cleanliness, 1) if total_cleanliness > 0 else 0
            rating_data["average_value_for_money_rating"] = round(
                value_for_money_ratings / total_value_for_money, 1) if total_value_for_money > 0 else 0

            # Calculate overall average rating across all categories
            total_avg_rating = 0
            rating_categories = [
                rating_data["average_behavior_rating"],
                rating_data["average_service_rating"],
                rating_data["average_quality_rating"],
                rating_data["average_cleanliness_rating"],
                rating_data["average_value_for_money_rating"]
            ]

            # Only include non-zero ratings in overall average
            non_zero_ratings = [rating for rating in rating_categories if rating > 0]
            if non_zero_ratings:
                total_avg_rating = sum(non_zero_ratings) / len(non_zero_ratings)

            rating_data["overall_average_rating"] = round(total_avg_rating, 1)


            response["rating_data"] = rating_data
            # Check if the current user has already rated the vendor
            response["current_user_rating"] = None
            if request.user.is_authenticated and not request.user.is_anonymous:
                current_user_rating = ratings.filter(user=request.user).first()
                if current_user_rating:
                    response["current_user_rating"] = {
                        "behavior_rating": current_user_rating.behavior_rating,
                        "service_rating": current_user_rating.service_rating,
                        "quality_rating": current_user_rating.quality_rating,
                        "cleanliness_rating": current_user_rating.cleanliness_rating,
                        "value_for_money_rating": current_user_rating.value_for_money_rating,
                    }

            return custom_response(
                success=True,
                data=response,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return custom_response(
                success=False,
                message="An error occurred while fetching vendor ratings.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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


        