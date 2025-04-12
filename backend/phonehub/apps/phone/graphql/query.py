import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry.types import Info
from typing import Optional
from phone.models import ContactTypeEnum

from django.db.models import Q
from django.db.models.query import QuerySet

from phone.models import Contact
from .types import (
    CallLogType,
    CallQueueType,
    ContactType,
    CallLogFilter,
    CallQueueFilter,
)

import logging


@strawberry.type
class Query:
    # Query to fetch all call logs
    call_logs: OffsetPaginated[CallLogType] = strawberry_django.offset_paginated(
        filters=CallLogFilter
    )

    # Query to fetch all call queues
    call_queues: OffsetPaginated[CallQueueType] = strawberry_django.offset_paginated(
        filters=CallQueueFilter
    )

    # Query to fetch all contacts, with an optional search parameter
    @strawberry_django.offset_paginated(OffsetPaginated[ContactType])
    def contacts(self, info: Info, search: Optional[str] = None) -> QuerySet[Contact]:
        user = info.context.get("user")
        
        qs = Contact.objects.filter(
            Q(type__in=[ContactTypeEnum.INTERNAL, ContactTypeEnum.EXTERNAL]) |
            Q(type=ContactTypeEnum.PERSONAL, personal_contact_owner=user)
        )

        if search:
            search_filter = Q(firstname__icontains=search) | Q(lastname__icontains=search) | \
                            Q(prefixlastname__icontains=search) | Q(department__icontains=search) | \
                            Q(mobile_nr__icontains=search)
            qs = qs.filter(search_filter)

        return qs