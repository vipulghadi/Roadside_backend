from rest_framework import serializers
from .models import *
class VendorProfileSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField(read_only=True)
    role=serializers.SerializerMethodField(read_only=True)
    first_name=serializers.SerializerMethodField(read_only=True)
    last_name=serializers.SerializerMethodField(read_only=True)
    email=serializers.SerializerMethodField(read_only=True)
    contact_number=serializers.SerializerMethodField(read_only=True)
    
    def get_username(self, obj):
        return obj.owner.username
    
    def get_role(self, obj):
        return obj.owner.role
    
    def get_first_name(self, obj):
        return obj.owner.first_name
    
    def get_last_name(self, obj):
        return obj.owner.last_name
    
    def get_email(self, obj):
        return obj.owner.email
    
    def get_contact_number(self, obj):
        return obj.owner.contact_number
    
        
    class Meta:
        model = VendorProfile
        fields = '__all__'
        
class VendorShopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorShopType
        fields = '__all__'
        
class VendorImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorImages
        fields = '__all__'
        
class VendorFoodItemsSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True)
    image=serializers.SerializerMethodField(read_only=True)
    image_id=serializers.SerializerMethodField(read_only=True)
    def get_name(self, obj):
        return obj.food_item.name
    
    def get_image(self, obj):
        return obj.food_item.image
    
    def get_image_id(self, obj):
        return obj.food_item.id
    class Meta:
        model = VendorFoodItem
        fields = '__all__'
        

class VendorFoodItemImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorFoodItemImage
        fields = '__all__'
        

class VendorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorReview
        fields = '__all__'
        
class VendorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRating
        fields = '__all__'
        

        
        

        
        
        
        