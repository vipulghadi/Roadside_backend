from rest_framework import serializers
from .models import *

class GeneralIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralIssues
        fields="__all__"

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields="__all__"
class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketResponse
        fields="__all__"
