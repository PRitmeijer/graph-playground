import strawberry_django

from userstatus.models import UserStatus

@strawberry_django.type(
    model=UserStatus, 
    fields="__all__"
)
class UserStatusType:
    pass