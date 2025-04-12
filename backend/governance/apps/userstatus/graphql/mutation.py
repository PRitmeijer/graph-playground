import strawberry
import strawberry_django
from strawberry.types import Info

from .types import UserStatusType

@strawberry.type
class Mutation:
    @strawberry_django.mutation()
    def update_user_status(self, info: Info, user_id: int, status_id: int) -> UserStatusType:
        user =info.context.get("user")
        status = UserStatusType.objects.get(id=status_id)
        user.status = status
        user.save()
        return status