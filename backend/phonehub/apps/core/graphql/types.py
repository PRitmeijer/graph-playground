import strawberry_django

from core.models import PhoneUser

@strawberry_django.type(
    model=PhoneUser,
    fields=["id", "external_id", "pps_id"],
    pagination=True
)
class PhoneUserType:
    pass