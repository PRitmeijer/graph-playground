# federated_django.py
import strawberry
from strawberry_django.type import type as django_type
from typing import List


# Based on https://github.com/strawberry-graphql/strawberry-django/issues/59, but minimilized
# Couldn't get it working yet...
def federated_django_type(
    model,
    *,
    fields=strawberry.UNSET,
    filters=strawberry.UNSET,
    pagination=strawberry.UNSET,
    order=strawberry.UNSET,
    keys: List[str] = None,
    extend: bool = False,
    **kwargs,
):
    def wrapper(cls):
        # First wrap it with strawberry_django.type
        wrapped_cls = django_type(
            model=model,
            fields=fields,
            filters=filters,
            pagination=pagination,
            order=order,
            **kwargs,
        )(cls)

        # Then wrap it again with federation support
        return strawberry.federation.type(keys=keys or [], extend=extend)(wrapped_cls)

    return wrapper
