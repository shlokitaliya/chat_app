from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout as auth_logout

def home(request):
    """
    Render the home page of the chat application.
    This view is responsible for displaying the main interface of the chat app.
    
    """
    return render(request, "authenticate/home.html")


def login_view(request):
    """
    Render the login page for the chat application.
    This view is responsible for displaying the login form and handling user authentication.
    
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "No account is linked with this email.")
            return redirect('login_view')
        user = User.objects.get(email=email)
        if not check_password(password, user.password):
            messages.error(request, "Incorrect password.")
            return redirect('login_view')
        request.session['user_id'] = user.id
        # login(request, user)
        messages.success(request, "Login successful.")
        return redirect('chat_home')
    
        


    return render(request, "authenticate/login.html")


def logout_view(request):
    """
    Logs the user out by clearing their session data and redirects to the home page.
    """
    # We use a try/except block to prevent errors if a user who is not logged in
    # somehow tries to access this view.
    try:
        # The key 'user_id' is the one you set during login.
        # Deleting it from the session effectively logs the user out.
        del request.session['user_id']
        
        # Add a success message to inform the user.
        messages.success(request, "You have been successfully logged out.")
        
    except KeyError:
        # This will happen if 'user_id' was not in the session, which is fine.
        # We can just ignore it and proceed to the redirect.
        pass

    # Redirect the user to the 'home' page after logging them out.
    return redirect('home')


def signup_view(request):
    """
    Render the signup page for the chat application.
    This view is responsible for displaying the signup form and handling user registration.
    
    """
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
        
        if User.objects.filter(username = username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup_view')

        if User.objects.filter(email = email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup_view')
        hashes_password = make_password(password)
        user = User(username = username,email = email, password = hashes_password)
        user.save()
        messages.success(request, "User created successfully.")
        return redirect('login_view')
    return render(request, "authenticate/signup.html")



