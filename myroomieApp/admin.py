from django.contrib import admin
from .models import Room, Profile, Message, RoomMember

@admin.register(Room)
class RoomModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_name', 'status', 'user']

@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'sender', 'message']

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio', 'image']

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'member']