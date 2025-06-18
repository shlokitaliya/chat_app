from django.shortcuts import render
from django.http import HttpResponse
from authentication.models import User

def chat_home(request):
    """
    Render the chat home page of the chat application.
    This view is responsible for displaying the main interface of the chat app.
    
    """
    code = User.objects.get(username='shlok').unique_code
    return render(request, "chat/chat_home.html",{"code":code})
