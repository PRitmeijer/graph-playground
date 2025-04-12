from django.db import models

class PhoneUser(models.Model):
    """
    Model to represent a user in the phone system.
    Reference object to the core user in microservice Governance.
    Gets attached as user in the middleware.
    Not to be confused with Django Users.
    """

    external_id = models.IntegerField(
        null=False,
        blank=False,
        db_index=True,
        help_text="The user this phone user belongs to"
    )

    pps_id = models.IntegerField(
        null=False,
        blank=False,
        db_index=True,
        help_text="The PPS ID of the user",
    )
