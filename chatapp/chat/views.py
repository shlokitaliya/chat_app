from django.shortcuts import render, redirect
from django.http import HttpResponse
from authentication.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.http import JsonResponse

@login_required
def chat_home(request):
    """
    Render the chat home page of the chat application.
    This view is responsible for displaying the main interface of the chat app.
    
    """
    user = request.user
    friends = get_friends(user)

    friends_with_last_msg = []

    for friend in friends:
        last_msg = PrivateChat.objects.filter(
            (Q(sender = user) & Q(receiver = friend)) |
            (Q(sender = friend) & Q(receiver = user))
        ).order_by('-timestamp').first()

        friends_with_last_msg.append({
            'user': friend,
            'last_msg': last_msg.message if last_msg else "Start a new chat",
            'room_name': generate_room_name(user,friend)
        })

    return render(request, "chat/chat_home.html",{'friends':friends_with_last_msg})


# function to generate unique room names for private
def generate_room_name(user,friend):
    userID = user.unique_code
    friendID = friend.unique_code
    sorted_codes = sorted([userID,friendID])
    return f'{sorted_codes[0]}_{sorted_codes[1]}'

@login_required
def add_friend(request):
    if request.method == "POST":
        user = request.user
        friendID = request.POST.get('friend_code','').strip().upper()

        try:
            friend = User.objects.get(unique_code = friendID)
            if friend != request.user:
                add_friend_db(user,friend)
                messages.success(request, f"{friend.username} added as a friend.")
            else:
                messages.warning(request, "You can't add Yourself.")
        except User.DoesNotExist:
            messages.error(request, "No user found with that code.")
    return redirect('chat_home')

@login_required
def fetch_private_messages(request, friend_id):
    try:
        user = request.user
        friend = User.objects.get(id = friend_id)


        messages = PrivateChat.objects.filter(
            sender__in = [user,friend] ,
            receiver__in = [user, friend]
        ).order_by('timestamp')
    
        print("User:", user, "Friend ID:", friend_id)
        print("Query returned:", messages)

        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                'message': msg.message,
                'timestamp': DateFormat(msg.timestamp).format('d M Y, h:i A'),
                'is_sender': msg.sender == user
            })
        
        return JsonResponse(formatted_messages, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Friend not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
