from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from chat_support.models import ChatAssistantConversationRoom
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        query_params = parse_qs(self.scope['query_string'].decode('utf-8'))
        self.access_token = query_params.get('access_token', [None])[0]
        self.is_anonymous = query_params.get('is_anonymous', ['false'])[0] == 'true'
        self.sender_id = query_params.get('sender_id', [None])[0]

        try:
            # Validate the room
            room = await self.validate_room()
            if not room:
                await self.close(reason="Room not found.")
                return

            # Validate user based on anonymity status and access token
            if self.is_anonymous:
                if not self.sender_id:
                    await self.close(reason="Access denied: sender_id missing for anonymous user.")
                await self.validate_anonymous_user(room)
                self.is_normal_user = True
            else:
                user = await self.validate_authenticated_user(room)
                if user == room.user:  # Check if authenticated user is the "user" or "assistant"
                    self.is_normal_user = True
                elif user == room.assistant:
                    self.is_normal_user = False  # Assistant is not a normal user

        except Exception as e:
            await self.close(reason=str(e))
            return

        # Define the room group name
        self.room_group_name = f"chat_{self.room_id}"

        # Add the WebSocket to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        try:
            # Remove the WebSocket from the room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            print(f"Error during disconnect: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')

            # Only broadcast non-empty messages
            if message:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": message,
                        "is_anonymous": self.is_anonymous,
                        "is_normal_user": self.is_normal_user  # Include the is_normal_user flag
                    }
                )
        except Exception as e:
            print(f"Error during receive: {e}")
            await self.close()

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                "message": event['message'],
                "is_anonymous": event['is_anonymous'],
                "is_normal_user": event['is_normal_user']  # Include the is_normal_user flag
            }))
        except Exception as e:
            print(f"Error during chat_message: {e}")

    @database_sync_to_async
    def validate_room(self):
        try:
            return ChatAssistantConversationRoom.objects.get(room_id=self.room_id)
        except ChatAssistantConversationRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def validate_anonymous_user(self, room):
        try:
            if room.anonymous_user != self.sender_id:
                raise DenyConnection("Access denied: Invalid sender_id for anonymous user.")
        except Exception as e:
            raise DenyConnection(f"Error validating anonymous user: {e}")

    async def validate_authenticated_user(self, room):
        try:
            user = await self.authenticate_access_token(self.access_token)

            # Check if the user is either the room's user or assistant
            if room.user==user:
                self.is_normal_user = True
                return user
            elif room.assistant==user:
                self.is_normal_user = False  # Assistant is not a normal user
                return user
            else:
                raise DenyConnection("Access denied: Unauthorized authenticated user.")
        except AuthenticationFailed as e:
            raise DenyConnection(f"Authentication failed: {e}")
        except Exception as e:
            raise DenyConnection(f"Error validating authenticated user: {e}")

    @database_sync_to_async
    def authenticate_access_token(self, token):
        """
        Validates the access token and retrieves the associated user.
        """
        if not token:
            raise AuthenticationFailed("Access token is missing.")

        try:
            token_obj = AccessToken(token)
            user = User.objects.get(id=token_obj['user_id'])
            return user
        except Exception as e:
            raise AuthenticationFailed(f"Invalid access token: {e}")
