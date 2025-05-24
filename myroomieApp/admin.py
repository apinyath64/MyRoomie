from django.contrib import admin
from .models import Room, Profile, Message, RoomMember, Notification, MemberRequest
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff']

@admin.register(Room)
class RoomModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_name', 'status', 'user', 'is_private']

@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'sender', 'message']

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio', 'image']

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'member']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'created_at', 'is_read']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(MemberRequest)