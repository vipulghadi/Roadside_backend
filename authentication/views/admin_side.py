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

class GoogleOAuthAPI(APIView):
    def get(self, request):...
    def post(self, request):...


