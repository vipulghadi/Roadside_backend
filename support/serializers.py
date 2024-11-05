from rest_framework import serializers
from .models import *

class GeneralIssuesSerializer(serializers.Serializer):
    class Meta:
        model = GeneralIssues
        fields="__all__"

class TicketSerializer(serializers.Serializer):
    class Meta:
        model = Ticket
        fields="__all__"
class TicketResponseSerializer(serializers.Serializer):
    class Meta:
        model = TicketResponse
        fields="__all__"
