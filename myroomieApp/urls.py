from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('profile/<int:user_id>/<str:username>/', views.profile_user, name='profile'),
    path('profile-setting/', views.ProfileSettingView.as_view(), name='profile_setting'),
    path('create-chat-room/', views.create_chat_room, name='create_chat_room'),
    path('<int:room_id>/<str:room_name>/<str:username>/', views.message_view, name='room'),
    path('add-room-member/<int:room_id>/<str:username>/', views.add_room_member, name='add_room_member'),
    path('change_status/<int:room_id>/', views.change_status, name='change_status'),
    
]