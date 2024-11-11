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
from support.models import *


class GeneralIssueListCreate(ListAPIView):
    serializer_class = GeneralIssuesSerializer
    pagination_class = PaginationSize20
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = GeneralIssues.objects.filter(is_deleted=False).order_by('-id')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_param = self.request.query_params.get("page")
        if page_param:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return custom_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return custom_response(
                data=serializer.data,
                status=status.HTTP_200_OK,
                success=True)
    
    def post(self, request, *args, **kwargs):
        serializer = GeneralIssuesSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(serializer.data, status=status.HTTP_201_CREATED)
        return custom_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneralIssueDetail(APIView):
    def get_object(self,pk):
        try:
            return GeneralIssues.objects.get(pk=pk, is_deleted=False)
        except GeneralIssues.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = GeneralIssuesSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = GeneralIssuesSerializer(inst, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return custom_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.delete()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )
    
        

class TicketListAPI(ListAPIView):
    serializer_class = TicketSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        queryset = Ticket.objects.filter(is_deleted=False).order_by('-id')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_param = self.request.query_params.get("page")
        if page_param:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return custom_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return custom_response(serializer.data)
        

class TicketReponseListCreate(ListAPIView):
    serializer_class = TicketResponseSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = PaginationSize20
    
    def get_queryset(self):
        queryset = TicketResponse.objects.filter(is_deleted=False).order_by('-id')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_param = self.request.query_params.get("page")
        if page_param:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return custom_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return custom_response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = TicketResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(serializer.data, status=status.HTTP_201_CREATED)
        return custom_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TicketResponseDetail(APIView):
    def get_object(self,pk):
        try:
            return TicketResponse.objects.get(pk=pk, is_deleted=False)
        except TicketResponse.DoesNotExist:
            raise Http404("not found")
    
    def get(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = TicketResponseSerializer(inst)
        return custom_response(
            success=True,
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, format=None):
        inst = self.get_object(pk)
        serializer = TicketResponseSerializer(inst, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=True,
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return custom_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inst = self.get_object(pk)
        inst.delete()
        return custom_response(
            success=True,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )
        
    
        