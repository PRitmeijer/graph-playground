import strawberry
import strawberry_django
from typing import List

from .types import UserType

@strawberry.type
class Query:
    # Query to fetch all users
    users: List[UserType] = strawberry_django.field()
    