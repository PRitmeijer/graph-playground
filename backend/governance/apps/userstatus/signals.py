from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from userstatus.models import UserStatus

@receiver(post_save, sender=get_user_model())
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserStatus.objects.create(
            user=instance, 
            reason="unavailable",
            mode="logged_out")
        
@receiver([user_logged_in, user_logged_out])
def update_user_status(sender, request, user, **kwargs):
    
    # is_authenticated is check if passed user is anonymous user or not, not login status.
    if user.is_authenticated:
        status = UserStatus.objects.get(user=user.id)
        if sender == user_logged_in:
            # Assuming user wants to control reason themselves.
            status.mode = "idle"
        elif sender == user_logged_out:
            status.reason = "unavailable"
            status.mode = "logged_out"
        status.save()