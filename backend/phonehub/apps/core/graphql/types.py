import strawberry
import strawberry_django
from core.models import CustomUser as User

@strawberry_django.type(
    model=User, 
    fields=["id", "email", "first_name", "last_name", "is_active", "date_joined"]
)
class UserType:
    pass