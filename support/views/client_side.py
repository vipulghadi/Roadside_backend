from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import Http404

from Roadside_backend.pagination import PaginationSize20
from Roadside_backend.utils import custom_response
from support.serializers import *

class CreateTicketAPI(APIView):
    def post(self, request, *args, **kwargs):
        request_data=request.data.copy()
        request_data["raise_by"]=request.user.id
        serializer=TicketSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return custom_response(
                success=False,
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )



            
        
        
        
    
    
    