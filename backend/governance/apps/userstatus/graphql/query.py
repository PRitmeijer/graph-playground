import strawberry
import strawberry_django
from typing import List

from .types import UserStatusType

@strawberry.type
class Query:
    # Query to fetch all user statuses
    user_statuses: List[UserStatusType] = strawberry_django.field()