from django.db import models
import uuid
import random
import string

# Create your models here.

def auto_generate_special_id():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not User.objects.filter(unique_code=code).exists():
            return code
        
def generate_group_code():
    length = 8
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Group.objects.filter(group_code=code).exists():
            return code

class User(models.Model):

    class GenderTypes(models.TextChoices):
        MALE = 'Male','Male'
        FEMALE = 'Female','Female'
        OTHER = 'Other','Other'
        FREFER_NOT_TO_SAY = 'Prefer not to say','Prefer not to say'

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    unique_code = models.CharField(max_length=6, unique=True, editable=False, default=auto_generate_special_id)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    profile_picture = models.ImageField(upload_to='profile_pic/users/',default='profile_pic/default.png',null=True,blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GenderTypes.choices, null=True, blank=True)
    # phone_number = models.CharField(max_length=15, null=True, blank=True)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

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
    members = models.ManyToManyField(User, related_name='groups')
    profile_pic = models.ImageField(upload_to='group_pics/', default='group_pics/default.png', null=True, blank=True)
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

