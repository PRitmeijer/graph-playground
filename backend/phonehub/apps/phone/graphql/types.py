import strawberry_django
from strawberry import ID, enum, auto
from typing import List, Optional

from core.graphql.types import PhoneUserType
from phone.models import CallLog, CallQueue, Contact

@strawberry_django.filter(CallQueue, lookups=["exact", "icontains"])
class CallQueueFilter:
    id: auto
    name: auto

@strawberry_django.type(
    model=CallQueue,
    fields=["id", "name"],
    filters=CallQueueFilter,
)
class CallQueueType:
    members: List[PhoneUserType]


@strawberry_django.filter(CallLog, lookups=True)
class CallLogFilter:
    id: auto
    start_time: auto
    end_time: auto
    duration_seconds: auto
    direction: auto
    caller_id: auto


@strawberry_django.type(
    model=CallLog, 
    fields=["id", "start_time", "end_time", "duration_seconds", "caller_id", "callee_id", "direction"],
    filters=CallLogFilter,
    pagination=True
)
class CallLogType:
    user: PhoneUserType
    call_queue: Optional[CallQueueType]

@strawberry_django.type(
    model=Contact, 
    fields=["id", "firstname", "prefixlastname", "lastname", "mobile_nr", "landline_nr", "department", "type"],
    pagination=True
)
class ContactType:
    user: Optional[PhoneUserType]
