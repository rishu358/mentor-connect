from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
    # Get the actual User instance instead of the lazy object
        self.user = self.scope["user"]._wrapped if hasattr(self.scope["user"], "_wrapped") else self.scope["user"]
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name'] 
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        # Now add the resolved user instance
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()



    def disconnect(self, close_code):
    # Get the actual User instance
        self.user = self.scope["user"]._wrapped if hasattr(self.scope["user"], "_wrapped") else self.scope["user"]
    
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

    # Remove and update online users with resolved user instance
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()



    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = GroupMessage.objects.create(
            body = body,
            author = self.user, 
            group = self.chatroom 
        )
         
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )


    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message' : message,
            'users' : self.user
        }

        html = render_to_string("a_rtchat/partials/chat_message_p.html", context = context)
        self.send(text_data=html)


    def update_online_count(self):
        online_count = self.chatroom.users_online.count()
        
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)


    def online_count_handler(self, event):
        online_count = event['online_count']

        context = {
            'online_count' : online_count,
            'chat_group' : self.chatroom,
        }

        html = render_to_string("a_rtchat/partials/online_count.html", context)
        self.send(text_data=html) 


# a_rtchat/consumers.py
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Only allow authenticated users
        if self.scope["user"].is_authenticated:
            self.accept()
            # Get the room name from the URL
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'
            
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            
            if hasattr(self, 'chatroom') and self.chatroom:
                self.chatroom.users_online.add(self.scope["user"])
        else:
            self.close()