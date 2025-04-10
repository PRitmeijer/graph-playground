import strawberry
import strawberry_django
from typing import List

from .types import CallLogType, CallQueueType, ContactType

@strawberry.type
class Query:
    # Query to fetch all call logs
    call_logs: List[CallLogType] = strawberry_django.field()

    # Query to fetch all call queues
    call_queues: List[CallQueueType] = strawberry_django.field()
    
    # Query to fetch all contacts
    contacts: List[ContactType] = strawberry_django.field()