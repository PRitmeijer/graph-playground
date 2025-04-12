from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class UserStatus(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_status',
        db_index=True,
        help_text="The user this status belongs to."
    )

    reason = models.CharField(
        max_length=50,
        help_text="Reason for the user's mode, e.g., 'lunch', 'available', 'training', 'unavailable'."
    )
    mode = models.CharField(
        max_length=50,
        help_text="System mode of the user's activity, e.g., 'idle', 'calling', 'logged_out'."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username