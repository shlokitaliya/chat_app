from django.db import models
import uuid
import random
import string
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

from django.db import connection

def auto_generate_special_id():
    from authentication.models import User  # local import to avoid issues
    length = 6

    # Check if the table exists
    if 'authentication_user' not in connection.introspection.table_names():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not User.objects.filter(unique_code=code).exists():
            return code

        
def generate_group_code():
    from authentication.models import Group  # local import
    length = 8

    if 'authentication_group' not in connection.introspection.table_names():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Group.objects.filter(group_code=code).exists():
            return code
class User(AbstractUser):

    class GenderTypes(models.TextChoices):
        MALE = 'Male','Male'
        FEMALE = 'Female','Female'
        OTHER = 'Other','Other'
        FREFER_NOT_TO_SAY = 'Prefer not to say','Prefer not to say'

     # Extra fields
    unique_code = models.CharField(max_length=6, unique=True, editable=False, default=auto_generate_special_id)
    profile_picture = models.ImageField(upload_to='profile_pic/users/', default='profile_pic/default.svg', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GenderTypes.choices, null=True, blank=True)

    def __str__(self):
        return self.username

class PrivateChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField(max_length=500)
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"chat from {self.sender.unique_code} to {self.receiver.unique_code} at {self.timestamp}"
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    group_code = models.CharField(max_length=8, unique=True, default=generate_group_code, editable=False)
    members = models.ManyToManyField(User, related_name='chat_groups')
    profile_pic = models.ImageField(upload_to='group_pics/', default='group_pics/default.svg', null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.group_code}) created by {self.created_by.username if self.created_by else 'Unknown'}"
    
class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    attachment = models.FileField(upload_to='group_attachments/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read_by = models.ManyToManyField(User, related_name='read_group_messages', blank=True)

    def __str__(self):
        return f"{self.sender.unique_code} in {self.group.name}: {self.message[:20]}"

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} ↔ {self.friend.username}"

def add_friend_db(user1, user2):
    Friendship.objects.get_or_create(user=user1, friend=user2)
    Friendship.objects.get_or_create(user=user2, friend=user1)

def get_friends(user):
    return User.objects.filter(related_to__user=user)