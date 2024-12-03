from django.http import JsonResponse
from users.models import StaffUserProfile, User  # Assuming User model contains `is_online` or similar field
from .models import ChatAssistantConversationRoom, ChatAssistantConversation
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import transaction

from Roadside_backend.utils import custom_response

class ConnectToRoomApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            with transaction.atomic():
                user = request.user if request.user.is_authenticated else None
                print(user)
                # Check for existing room for the authenticated user
                if user:
                    chat_room = ChatAssistantConversationRoom.objects.filter(
                        user=user,
                        is_conversation_end=False
                    ).last()
                    
                    if chat_room:
                        return custom_response(
                            success=True,
                            data={
                                "room_id": room.room_id,
                                "is_anonymous_user":room.is_anonymous_user,
                                "anonymous_user":room.anonymous_user,
                                "chat_assistant_username": room.assistant.username,
                                "chat_assistant_id": room.assistant.id,
                                "first_name": room.assistant.first_name,
                                "last_name": room.assistant.last_name
                            },
                            status=200
                        )
                    else:
                        online_chat_assistant = StaffUserProfile.objects.filter(
                            designation="chat_assistant",
                            is_online=True,
                            is_free=True
                        ).first()
                        if online_chat_assistant:
                            chat_room=ChatAssistantConversationRoom.objects.create(
                                user=user,
                                chat_assistant=online_chat_assistant.user
                            )
                            online_chat_assistant.is_free = False
                            online_chat_assistant.save()
                            return custom_response(
                                success=True,
                                data={
                                "room_id": room.room_id,
                                "is_anonymous_user":room.is_anonymous_user,
                                "anonymous_user":room.anonymous_user,
                                "chat_assistant_username": room.assistant.username,
                                "chat_assistant_id": room.assistant.id,
                                "first_name": room.assistant.first_name,
                                "last_name": room.assistant.last_name
                                },
                                status=200
                            )
                        else:
                            bot_assistant = StaffUserProfile.objects.filter(
                            designation="chatbot").first()
                            room = ChatAssistantConversationRoom.objects.create(
                            user=user,  
                            assistant=bot_assistant.user
                        )
                            return custom_response(
                                success=True,
                                data={
                                "room_id": room.room_id,
                                "is_anonymous_user":room.is_anonymous_user,
                                "anonymous_user":room.anonymous_user,
                                "chat_assistant_username": room.assistant.username,
                                "first_name": room.assistant.first_name,
                                "last_name": room.assistant.last_name,
                                "chat_assistant_id": room.assistant.id,
                                },
                                status=200
                            )
                            
                # Handle anonymous users or new room creation
                else:
                    chat_assistant = StaffUserProfile.objects.filter(
                            designation="chat_assistant",
                            is_online=True,
                            is_free=True
                        ).first()
                    
                    if chat_assistant:
                            chat_room=ChatAssistantConversationRoom.objects.create(
                                is_anonymous_user=True,
                                chat_assistant=chat_assistant.user
                            )
                            chat_assistant.is_free = False
                            chat_assistant.save()

                    else:
                        bot_assistant = StaffUserProfile.objects.filter(
                            designation="chatbot"
                            ).first()
                        room = ChatAssistantConversationRoom.objects.create(
                        is_anonymous_user=True,
                        assistant=bot_assistant.user
                    )
                        return custom_response(
                            success=True,
                            data={
                                "room_id": room.room_id,
                                "is_anonymous_user":room.is_anonymous_user,
                                "anonymous_user":room.anonymous_user,
                                "chat_assistant_username": room.assistant.username,
                                "chat_assistant_id": room.assistant.id,
                                "first_name": room.assistant.first_name,
                                "last_name": room.assistant.last_name
                            },
                            status=200
                        )

        except Exception as e:
            print(e)
            return custom_response(
                success=False,
                message="An error occurred while connecting to the room.",
                status=500
            )


                        
            
            
            
            
            
        
        
            
    
        
        
        
        
class StartConversationAPI(APIView):
    def post(self, request):
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
