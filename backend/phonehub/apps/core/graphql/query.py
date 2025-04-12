import strawberry
import strawberry_django
from typing import List
from core.graphql.types import PhoneUserType

@strawberry.type
class Query:
    # Query to all phone users
    phone_users:List[PhoneUserType] = strawberry_django.field()