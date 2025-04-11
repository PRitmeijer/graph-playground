import strawberry
import strawberry_django
from typing import List, Optional
from strawberry_django.pagination import OffsetPaginated
from django.db.models.query import QuerySet
from django.db.models import Q
from phone.models import Contact
from .types import CallLogType, CallQueueType, ContactType

@strawberry.type
class Query:
    # Query to fetch all call logs
    call_logs: List[CallLogType] = strawberry_django.field()

    # Query to fetch all call queues
    call_queues: List[CallQueueType] = strawberry_django.field()
    
    # Query to fetch all contacts, with search option
    @strawberry_django.offset_paginated(OffsetPaginated[ContactType])
    def contacts(self, search: Optional[str] = None) -> QuerySet[Contact]:
        qs = Contact.objects.all()
        if search:
            qs = qs.filter(
                Q(firstname__icontains=search) |
                Q(lastname__icontains=search) |
                Q(prefixlastname__icontains=search) |
                Q(department__icontains=search) |
                Q(mobile_nr__icontains=search)
            )
        return qs