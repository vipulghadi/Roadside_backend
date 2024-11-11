
from django.contrib import admin
from django.urls import path
from support.views.client_side import *

urlpatterns = [
    path('raise-ticket/', CreateTicketAPI.as_view(),name='ticket-list'),
]