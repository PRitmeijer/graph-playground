import strawberry
import strawberry_django
from typing import Optional
from django.contrib.auth import get_user_model

from userstatus.graphql.types import UserStatusType

User = get_user_model()

@strawberry_django.type(
    model=User, 
    fields=[
        "id",
        "email",
        "first_name",
        "prefix_last_name",
        "last_name",
        "is_active",
        "date_joined",
    ]
)
class UserType:
    status: Optional["UserStatusType"] = strawberry_django.field(
        resolver=lambda root: root.user_status
    )

def get_user(root: "PhoneUserType") -> "UserType":
    return User.objects.get(pk=root.external_id)

@strawberry.federation.type(keys=["externalId"], extend=True)
class PhoneUserType:
    external_id: int = strawberry.federation.field(external=True, name="externalId")
    user: UserType = strawberry_django.field(resolver=get_user)