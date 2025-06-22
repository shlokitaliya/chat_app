from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout, authenticate



def home(request):
    """
    Render the home page of the chat application.
    This view is responsible for displaying the main interface of the chat app.
    
    """
    return render(request, "authenticate/home.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)  # this sets session and user
            messages.success(request, "Login successful.")
            return redirect('chat_home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login_view')

    return render(request, "authenticate/login.html")
        




def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup_view')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup_view')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup_view')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup_view')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password  # `create_user` hashes it internally
        )

        messages.success(request, "Signup successful! Please login.")
        return redirect('login_view')

    return render(request, "authenticate/signup.html")


