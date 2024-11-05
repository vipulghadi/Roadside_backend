# tickets/models.py
from django.db import models
from django.contrib.auth.models import User
from food_items.models import BaseModel

class GeneralIssues(BaseModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "General Issues"
        db_table = "general_issues"
    
    def __str__(self):
        return self.title
    
class Ticket(BaseModel):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    issue_type=models.ForeignKey(GeneralIssues,on_delete=models.SET_NULL,blank=True,null=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    raise_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tickets"
        db_table = "tickets"
    def __str__(self):
        return self.title


class TicketResponse(BaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses',blank=True,null=True)
    response_text = models.TextField(blank=True, null=True)
    response_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    response_to=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Ticket Responses"
        db_table = "ticket_responses"
    
    def __str__(self):
        return f"{self.ticket.title} - Response {self.id}"
    

    
    
