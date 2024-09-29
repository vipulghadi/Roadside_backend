from rest_framework import serializers
from .models import *


class CreateUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'first_name', 'last_name',"username"]

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

