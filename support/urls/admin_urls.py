
from django.contrib import admin
from django.urls import path
from support.views.admin_side import *

urlpatterns = [
    path('ticket-list/', TicketListAPI.as_view(),name='ticket-list'),
    path('ticket-response/', TicketReponseListCreate.as_view(),name='ticket-response-list-create'),
    path('ticket-response/<pk>/', TicketResponseDetail.as_view(),name='ticket-response-detail'),
    path('general-issues/', GeneralIssueListCreate.as_view(),name='general-issues'),
    path('general-issues/<pk>/', GeneralIssueDetail.as_view(),name='general-issues-detail'),
    
    
]