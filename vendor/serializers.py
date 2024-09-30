from rest_framework import serializers
from .models import *
class VendorProfileSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = VendorFoodItem
        fields = '__all__'
        

class VendorFoodItemImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorFoodItemImage
        fields = '__all__'
        
class VendorLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorLikes
        fields = '__all__'
        
class VendorDislikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDislikes
        fields = '__all__'

class VendorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorReview
        fields = '__all__'
        
class VendorReviewLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorReviewLikes
        fields = '__all__'
        
class VendorReviewDislikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorReviewLikes
        fields = '__all__'


        
        

        
        
        
        