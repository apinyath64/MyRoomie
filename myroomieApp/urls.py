from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('notification/', views.notification, name='notification'),
    path('profile/<int:user_id>/<str:username>/', views.profile_user, name='profile'),
    path('profile-setting/', views.ProfileSettingView.as_view(), name='profile_setting'),
    path('create-chat-room/', views.create_chat_room, name='create_chat_room'),
    path('<int:room_id>/<str:room_name>/<str:username>/', views.message_view, name='room'),
    path('room_confirm_delete/<int:room_id>/', views.room_confirm_delete, name='room_confirm_delete'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('add-room-member/<int:room_id>/<str:username>/', views.add_room_member, name='add_room_member'),
    path('change_status/<int:room_id>/', views.change_status, name='change_status'),
    path('removemember/', views.remove_member),
    path('send-member-request/<int:room_id>/', views.member_request, name='send-member-request'),
    path('accept-member-request/<int:request_id>/', views.member_accept, name='accept-member-request'),
    
]