from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="ชื่อผู่ใช้", widget=forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))
    email = forms.EmailField(label="อีเมล", widget=forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))
    password1 = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))
    password2 = forms.CharField(label="ยืนยันรหัสผ่าน", widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SignInForm(AuthenticationForm):
    username = forms.CharField(label="ชื่อผู้ใช้", widget=forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))
    password = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'}))


class ChatRoomForm(forms.ModelForm):
    room_name = forms.CharField(label="ชื่อห้อง", widget=forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-[#575042] text-sm rounded-lg focus:ring-gray-600 focus:border-gray-600 block w-full p-2.5'}))
    
    class Meta:
        model = Room
        fields = ['room_name', 'status']

        labels = {
            'status': 'สถานะ',
            
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-[#575042] text-sm rounded-lg focus:ring-gray-600 focus:border-gray-600 block w-full p-2.5'})
        }
    

class ProfileSettingForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']



class AddRoomMember(forms.ModelForm):
    class Meta:
        model = RoomMember
        fields = ['member']


class ChangeRoomStatusForm(forms.ModelForm):
    # status = forms.CharField(widget=forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-[#575042] text-sm rounded-lg focus:ring-gray-600 focus:border-gray-600 block w-full p-2.5'}))
    class Meta:
        model = Room
        fields = ['status']