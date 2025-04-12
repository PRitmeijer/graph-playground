from django.db import models
from core.models import PhoneUser

# Create your models here.
class CallLog(models.Model):
    start_time = models.DateTimeField(help_text="Call start time")
    end_time = models.DateTimeField(help_text="Call end time")
    duration_seconds = models.PositiveIntegerField(help_text="Call duration in seconds")
    caller_id = models.CharField(
        max_length=50,
        help_text="Identifier for the caller (could be a phone number or reference ID)"
    )
    callee_id = models.CharField(
        max_length=50,
        help_text="Identifier for the callee (could be a phone number or reference ID)"
    )
    DIRECTION_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing')
    ]
    direction = models.CharField(
        max_length=10,
        choices=DIRECTION_CHOICES,
        help_text="Direction of the call"
    )
    # Optional link to a call queue; if the call did not go through a queue, this may be empty.
    call_queue = models.ForeignKey(
        'CallQueue',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='calls',
        help_text="Call queue associated with the call, if any"
    )
    # Link this call record to a user (the call history for that user)
    user = models.ForeignKey(
        PhoneUser,
        related_name='call_logs',
        on_delete=models.SET_NULL,
        null=True,
        db_index=True,
        help_text="User associated with this call log entry",
    )

    def __str__(self):
        return f"Call {self.pk}: {self.caller_id} -> {self.callee_id}"

# --- CallQueue Model ---
class CallQueue(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Name of the call queue"
    )

    # ManyTo-many relationship with Users: a queue can have multiple members and a user can belong to multiple queues.
    members = models.ManyToManyField(
        PhoneUser,
        related_name='call_queues',
        blank=True,
        help_text="Users that are members of this call queue"
    )

    def __str__(self):
        return self.name


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
        ('personal', 'Personal')
    ]

    firstname = models.CharField(
        max_length=100,
        help_text="First name"
    )

    prefixlastname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Prefix of the last name (if any)"
    )

    lastname = models.CharField(
        max_length=100,
        help_text="Last name"
    )

    mobile_nr = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Mobile phone number"
    )

    landline_nr = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Landline number or extension"
    )

    # For internal contacts, we link directly to the local user of that contact.
    # For non‑internal contacts (external/personal) this field can be left empty.
    user = models.ForeignKey(
        PhoneUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='contacts',
        help_text="Link to the user"

    )

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Department name (if applicable)"
    )

    type = models.CharField(
        max_length=10,
        choices=CONTACT_TYPE_CHOICES,
        db_index=True,
        help_text="Contact type: internal, external, or personal"
    )

    personal_contact_owner = models.ForeignKey(
        PhoneUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='personal_contacts',
        help_text="User ID indicating the owner of this personal contact"
    )

    def initials(self):
        """Return the initials of the contact in uppercase, ensuring no null values"""
        return f"{(self.firstname or '')[:1].upper()}{(self.lastname or '')[:1].upper()}"
    
    def __str__(self):
        """Return a string representation of the contact"""
        return f"{self.firstname or ''} {self.prefix or ''}{self.lastname or ''}"