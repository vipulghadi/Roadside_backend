from django.http import JsonResponse
from users.models import User  # Assuming User model contains `is_online` or similar field
from .models import ChatAssistantConversationRoom, ChatAssistantConversation
from django.db.models import Q

def start_conversation(request):
    if request.method == "POST":
        user = request.user
        message = request.POST.get("message", "")

        online_staff = User.objects.filter(is_staff=True, is_online=True).first()
        if not online_staff:
            return JsonResponse({"error": "No staff member is currently online."}, status=400)

        # Check if a room already exists or create one
        room, created = ChatAssistantConversationRoom.objects.get_or_create(
            user=user, assistant=online_staff
        )

        # Save the message
        ChatAssistantConversation.objects.create(
            sender=user,
            room=room,
            message=message
        )


        return JsonResponse({
            "message": "Conversation started.",
            "room_id": room.id,
            "assistant": online_staff.username,
        })
