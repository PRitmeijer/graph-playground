import strawberry
import strawberry_django
from typing import List, Optional
from core.graphql.types import UserType
from phone.models import CallLog, CallQueue, Contact

@strawberry_django.type(model=CallQueue, fields=["id", "name"])
class CallQueueType:
    members: List[UserType]

@strawberry_django.type(
    model=CallLog, 
    fields=["id", "start_time", "end_time", "duration_seconds", "caller_id", "callee_id", "direction"]
)
class CallLogType:
    user: UserType
    call_queue: Optional[CallQueueType]

@strawberry_django.type(
    model=Contact, 
    fields=["id", "firstname", "prefixlastname", "lastname", "mobile_nr", "landline_nr", "department", "type"]
)
class ContactType:
    user: Optional[UserType]
