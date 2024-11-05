from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import Http404

from Roadside_backend.pagination import PaginationSize20
from Roadside_backend.utils import custom_response


class CreateTicketAPI(ListAPIView):...
    
    
    