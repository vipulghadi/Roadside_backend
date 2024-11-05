from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'contact_number', 'email', 'first_name', 'last_name', 'username','role']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        
class CreateUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'contact_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'contact_number', 'email', 'first_name', 'last_name',"username","role"]

class OTPSignupSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['contact_number', 'first_name', 'last_name',"role"]
        
        def validate_contact_number(self, value):
            if User.objects.filter(contact_number=value,is_deleted=False).exists():
                raise serializers.ValidationError("Phone number already registered.")
            
            elif User.objects.filter(contact_number=value,is_deleted=True).exists():
                raise serializers.ValidationError("This accountis is blacklisted.")
            
            return value

