# Import your specific User model
from .models import User 
# Import the rest of the necessary modules from Django
from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=User)
def delete_user_sessions(sender, instance, **kwargs):
    """
    This function is a signal receiver that gets triggered after YOUR custom 
    User object is deleted. It finds and deletes all session data associated with that user.
    """
    # Find all sessions that have stored user data
    all_sessions = Session.objects.filter()
    
    # Iterate through each session
    for session in all_sessions:
        session_data = session.get_decoded()
        # Check if the session's user ID (using YOUR key 'user_id') 
        # matches the deleted user's ID.
        # We compare it as an integer since get_decoded() will deserialize it.
        if session_data.get('user_id') == instance.id:
            # If it matches, delete the session
            session.delete()
    
    print(f"All sessions for deleted user {instance.username} have been cleared.")