from django.db import models
from users.models import User
from food_items.models import BaseModel  

class ChatAssistantConversationRoom(BaseModel):
    """
    Represents a conversation room between a user and the chat assistant.
    """
    assistant = models.ForeignKey(
        User, 
        related_name='assistant_rooms',
        on_delete=models.SET_NULL, 
        null=True
    )
    user = models.ForeignKey(
        User, 
        related_name="user_conversations", 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"ConversationRoom {self.id} with {self.user.username}"

    class Meta:
        verbose_name_plural = "Conversation Rooms"


class ChatAssistantConversation(BaseModel):
    """
    Represents messages exchanged in a conversation room.
    """
    sender = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name="sent_messages", 
        null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(
        ChatAssistantConversationRoom, 
        on_delete=models.CASCADE, 
        related_name="messages"
    )
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Message by {self.sender.username if self.sender else 'Assistant'} in Room {self.room.id}"
