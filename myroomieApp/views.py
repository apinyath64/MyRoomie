from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, logout

def home(request):
    rooms = Room.objects.all()
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'rooms': rooms,
        'profile': profile
    }
    return render(request, 'index.html', context)


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ลงทะเบียนเข้าใช้งานสำเร็จ! ตอนนี้คุณสามารถเข้าสู่ระบบเพื่อเข้าใช้งานได้")
            return redirect('login')
        
        return render(request, 'signup.html', {'form': form})
    

class SignInView(View):
     def get(self, request):
          form = SignInForm()
          return render(request, 'login.html', {'form': form})
     
     def post(self, request):
            form = SignInForm(request, data=request.POST)
            if form.is_valid():
                 login(request, form.get_user())
                 return redirect('/')
            else:
                 messages.error(request, "ชื่อผู้ใข้หรือรหัสผ่านไม่ถูกต้อง!")

            return render(request, 'login.html', {'form': form})
     

def logout_user(request):
    logout(request)
    return redirect('login')


def profile_user(request, user_id, username):
    profile = []
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user__id=user_id)
        
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


class ProfileSettingView(View):
    def post(self, request):
        form = ProfileSettingForm()
        return render(request, 'profile_setting.html', {'form': form})
    

    def get(self, request):
        form = ProfileSettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_user')
        return render(request, 'profile_setting.html')
    


def create_chat_room(request):
    form = ChatRoomForm(request.POST)
    user = request.user
    if form.is_valid():
        room = form.save(commit=False)
        room.user = user
        member = user
        room.save()
        RoomMember.objects.create(room=room, member=member)

        messages.success(request, "สร้างห้องแชทสำเร็จ!")
        return redirect('/')
    
    return render(request, 'create_chat_room.html', {'form': form})


def message_view(request, room_id, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)
    room_members = RoomMember.objects.filter(room=room_id)

    room = get_object_or_404(Room, pk=room_id)
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    member_profile = []
    for member in room_members:
        try:
            p = Profile.objects.get(user=member.member)
        except Profile.DoesNotExist:
            p = None

        member_profile.append({
            'user': member.member,
            'member_profile': p 
        })

    context = {
        'room_id': room_id, 
        'room_name': room_name,
        'messages': get_messages,
        'user': username,
     
        'room': room,
        'profile': profile,
        'member_profile': member_profile
    }
    return render(request, 'message.html', context)


# def room_member(request, room_id):
#     get_room = Room.objects.get(pk=room_id)
#     get_members = RoomMember.objects.filter(room=get_room)

#     context = {
#         'room': get_room,
#         'members': get_members
#     }

#     return render(request, 'room_details.html', context)


def add_room_member(request, room_id, username):
    room = get_object_or_404(Room, pk=room_id)
    form = AddRoomMember()
    if request.method == 'POST':
        form = AddRoomMember(request.POST)
        if form.is_valid():
            member = RoomMember.objects.filter(room=room_id)
            member = form.cleaned_data['member']
            RoomMember.objects.create(room=room, member=member)
            return redirect('room', room_id=room_id, room_name=room.room_name, username=username)
        
    context = {
        'room': room,
        'form': form,  
        
    }
    return render(request, 'add_room_member.html', context)


def change_status(request, room_id):
    room = Room.objects.get(pk=room_id)
    username = request.user.username

    if request.method == 'POST':
        statusform = ChangeRoomStatusForm(request.POST, instance=room)
        if statusform.is_valid():
            # room.status = statusform.cleaned_data['status']
            statusform.save()
    return redirect('room', room_id=room_id, room_name=room.room_name, username=username)
    

        





