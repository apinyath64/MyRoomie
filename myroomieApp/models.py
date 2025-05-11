from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_STATUS = [
        ('A', 'Active'),
        ('CH', 'Chill'),
        ('D', 'Do Not Disturb'),
        ('S', 'Sleep')
    ]
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=200)
    status = models.CharField(max_length=100, choices=ROOM_STATUS, default='Active')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.room_name
    

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    
    def __str__(self):
        return f'{self.sender}| {self.message}'


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    image = models.ImageField(upload_to='profile')

    

class RoomMember(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

   