from django.db import models
from users.models import User
from food_items.models import BaseModel  
from  datetime import datetime
import string
import random

class ChatAssistantConversationRoom(BaseModel):
    """
    Represents a chat room between a user and an assistant, with optional anonymous mode.
    """
    assistant = models.ForeignKey(
        User,
        related_name='assistant_rooms',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The assistant participating in the conversation."
    )
    user = models.ForeignKey(
        User,
        related_name="user_conversations",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The user participating in the conversation."
    )
    is_anonymous_user = models.BooleanField(
        default=False,
        help_text="Indicates if the user is anonymous."
    )
    anonymous_user=models.CharField(max_length=255)
    room_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="Unique identifier for the conversation room."
    )
    is_conversation_end = models.BooleanField(
        default=False,
        help_text="Indicates if the conversation has ended."
    )

    def generate_room_id(self):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        if self.user and self.assistant:
            return f"{self.user.id}_{self.assistant.id}_{current_time}"
        elif self.is_anonymous_user:
            return f"anonymous_{current_time}"
        else:
            raise ValueError("Cannot generate room ID without user or assistant information.")
    def generate_unauthenticated_user_id(self):
        characters = string.ascii_letters + string.digits
        random_id = ''.join(random.choices(characters, k=15))
        return random_id
        
        
        
    def save(self, *args, **kwargs):
        if not self.room_id:
            self.room_id = self.generate_room_id()
        if not self.anonymous_user:
            self.anonymous_user = self.generate_unauthenticated_user_id() 
        super().save(*args, **kwargs)


    def __str__(self):
        if self.user:
            return f"ConversationRoom {self.id} with {self.user.username}"
        return f"ConversationRoom {self.id} (Anonymous)"

    class Meta:
        verbose_name_plural = "Conversation Rooms"
        ordering = ['-created_at']  

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
