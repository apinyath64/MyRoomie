from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import JsonResponse


def home(request):
    rooms = Room.objects.all()
    user = request.user
    room_member_request = MemberRequest.objects.all()

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    user_memberships = RoomMember.objects.filter(member=user)
    member_room_ids = user_memberships.values_list('room_id', flat=True)

    context = {
        'rooms': rooms,
        'profile': profile,
        'member_room_ids': member_room_ids,
        'room_member_request': room_member_request
        

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
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if form.is_valid():
        room = form.save(commit=False)
        room.user = user
        member = user
        room.save()
        RoomMember.objects.create(room=room, member=member)

        messages.success(request, "สร้างห้องแชทสำเร็จ!")
        return redirect('/')
    
    return render(request, 'create_chat_room.html', {'form': form, 'profile': profile})

def room_confirm_delete(request, room_id):
    room_details = get_object_or_404(Room, id=room_id, user=request.user)

    if request.user != room_details.user:
        redirect('home')

    context = {
        'room_details': room_details
    }
    return render(request, 'room_confirm_delete.html', context)

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "ลบห้องแชทสำเร็จ!")
        return redirect('home')


def message_view(request, room_id, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)
    room_members = RoomMember.objects.filter(room=room_id)
    room = get_object_or_404(Room, pk=room_id)

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    member_profile = []
    for r in room_members:
        try:
            p = Profile.objects.get(user=r.member)
        except Profile.DoesNotExist:
            p = None

        member_profile.append({
            'user': r.member,
            'member_profile': p,
            'member_id': r.id
        })
    
    if room.is_private and not RoomMember.objects.filter(room=room, member=request.user).exists():
        return redirect('home')

    context = {
        'room_id': room_id, 
        'room_name': room_name,
        'messages': get_messages,
        'user': username,
     
        'room': room,
        'profile': profile,
        'member_profile': member_profile,
        'room_members': room_members
    }
    return render(request, 'message.html', context)


def add_room_member(request, room_id, username):
    room = get_object_or_404(Room, pk=room_id)
    form = AddRoomMember()
    if request.method == 'POST':
        form = AddRoomMember(request.POST)
        
        if form.is_valid():
            member = form.cleaned_data['member']
            if RoomMember.objects.filter(room=room, member=member).exists():
                messages.error(request, "ผู้ใช้ดังกล่าวเป็นสมาชิกของห้องอยู่แล้ว")
                return redirect('add_room_member', room_id=room_id, username=username)
            else:
                RoomMember.objects.create(room=room, member=member)
                Notification.objects.create(user=member, message=f"คุณถูกเพิ่มไปยังห้อง {room.room_name}")
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
    

def remove_member(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member = get_object_or_404(RoomMember, id=member_id)
       
        member.delete()
        data = {
            'message': 'ลบสมาชิกจากห้องแชทสำเร็จ'
        }
    
    return JsonResponse(data)


def notification(request):
    user_notification = Notification.objects.filter(user=request.user, is_read=False)
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    context = {
        'user_notification': user_notification,
        'profile': profile
        
    }
    return render(request, 'notification.html', context)
        

def member_request(request, room_id):
    from_user = request.user
    to_room = get_object_or_404(Room, id=room_id)
    if to_room.user == from_user:
        messages.error(request, "คุณไม่สามารถส่งคำขอเข้าร่วมห้องแชทที่สร้างเองได้!")
        return redirect('home')
    
    # if member in room already exist
    if RoomMember.objects.filter(room=to_room, member=from_user).exists():
        messages.info(request, "คุณเป็นสมาชิกของห้องแชทอยู่แล้ว!")
        return redirect('home')

    member_request, created = MemberRequest.objects.get_or_create(from_user=from_user, to_room=to_room)
    if created:
        Notification.objects.create(user=to_room.user, message=f'คำขอเข้าร่วมห้องแชท {to_room.room_name} จาก {from_user.username}')
        messages.success(request, "ส่งคำขอเข้าร่วมห้องแชทแล้ว.")
        return redirect('home')
    else:
        messages.error(request, "คำขอเข้าร่วมห้องแชทถูกส่งแล้ว!")
        return redirect('home')
    

def member_accept(request, request_id):
    member_request = get_object_or_404(MemberRequest, id=request_id)
    if member_request.to_room.user == request.user:
        RoomMember.objects.create(room=member_request.to_room, member=member_request.from_user)
        Notification.objects.create(user=member_request.from_user, message=f'คุณถูกเพิ่มไปยังห้องแชท {member_request.to_room.room_name}')
        member_request.delete()
        messages.success(request, "เพิ่มสมาชิกห้องแชทสำเร็จ!")
        return redirect('home')
    else:
        messages.error(request, "เพิ่มสมาชิกไปยังห้องแชทไม่สำเร็จ!")
        return redirect('home')


