from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """
    Render the home page of the chat application.
    This view is responsible for displaying the main interface of the chat app.
    
    """
    return render(request, "authenticate/home.html")