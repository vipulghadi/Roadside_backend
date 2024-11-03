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



class OTPLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        contact_number = request.query_params.get('contact_number')
        if not contact_number:
            return custom_response(
                success=False,
                message="Phone number is required.",
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                contact_number=contact_number,
                
                defaults={'is_active': False}  # Set as inactive initially
            )
        

            # Generate OTP regardless of whether user is newly created or existing
            otp = generate_otp(contact_number)

        message = "OTP has been sent to your phone number."
        if created:
            message = "User created and OTP sent to your phone number."

        return custom_response(
            success=True,
            message=message,
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

        with transaction.atomic():
            if  not validate_otp(contact_number, otp) :
                try:
                    user = User.objects.get(contact_number=contact_number)
                    user.is_active = True
                    user.save()
                    
                    refresh = RefreshToken.for_user(user)
                    
                    return custom_response(
                        success=True,
                        message="OTP is valid. login successfull.",
                        data={
                            'refresh_token': str(refresh),
                            'access_token': str(refresh.access_token)
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

class GetCurrentUser(APIView):
    def get(self, request, *args, **kwargs):
        user=request.user
        user_data=UserDetailsSerializer(user).data
        return custom_response(
            data=user_data,
            message="success",
            success=True
        )
