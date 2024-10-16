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

class OTPSignupView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = OTPSignupSerializer(data=request.data)
        if serializer.is_valid():
            if not validate_phone_number(serializer.validated_data['contact_number']):
                return custom_response(
                    success=False,
                    message="Invalid contact number.",
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                contact_number=serializer.validated_data['contact_number'],
                is_active=True
            )
            user.set_unusable_password()  
            user.save()

            
            otp = generate_otp()

            return custom_response(
                success=True,
                message="User registered successfully. OTP sent to the user.",
                data={"otp": otp},
                status=status.HTTP_201_CREATED
            )
        else:
        
            return custom_response(
                success=False,
                message="Validation error",
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        contact_number = request.query_params.get('contact_number')
        otp = request.query_params.get('otp')

        if not contact_number or not otp:
            return custom_response(
                success=False,
                message="Both contact_number and otp are required.",
                status=status.HTTP_400_BAD_REQUEST
            )

        if validate_otp(contact_number, otp):
            try:
                user = User.objects.get(contact_number=contact_number)
                user.is_active = True
                user.save()
                refresh = RefreshToken.for_user(user)
                return custom_response(
                    success=True,
                    message="OTP is valid. Tokens generated.",
                    data={
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return custom_response(
                    success=False,
                    message="User with this contact number does not exist.",
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return custom_response(
                success=False,
                message="Invalid OTP.",
                status=status.HTTP_400_BAD_REQUEST
            )

class OTPLoginView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        contact_number = request.query_params.get('contact_number')
        if not contact_number:
            return custom_response(
                success=False,
                message="Phone number is required.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(contact_number=contact_number)
        except :
            return custom_response(
                success=False,
                message="User with this phone number does not exist.",
                status=status.HTTP_404_NOT_FOUND
            )
        
        otp = generate_otp(contact_number)

        
        return custom_response(
            success=True,
            message="OTP has been sent to your phone number.",
            data={"otp": otp},  
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        contact_number = request.data.get('contact_number')
        otp = request.data.get('otp')

        if not contact_number or not otp:
            return custom_response(
                success=False,
                message="Phone number and OTP are required.",
                status=status.HTTP_400_BAD_REQUEST
            )

        if validate_otp(contact_number, otp):
            try:
                user = User.objects.get(contact_number=contact_number)
                refresh = RefreshToken.for_user(user)
                
                return custom_response(
                    success=True,
                    message="OTP is valid. Tokens generated.",
                    data={
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return custom_response(
                    success=False,
                    message="User with this phone number does not exist.",
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return custom_response(
                success=False,
                message="Invalid OTP.",
                status=status.HTTP_400_BAD_REQUEST
            )
    