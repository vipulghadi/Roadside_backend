
from django.urls import path
from .views import *

urlpatterns = [
    path('connect-to-room/', ConnectToRoomApi.as_view(),name="connect-to-room"),
]
