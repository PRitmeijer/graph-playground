import strawberry
from core.graphql.query import Query as CoreQuery
from phone.graphql.query import Query as PhoneQuery
from strawberry_django.optimizer import DjangoOptimizerExtension

@strawberry.type
class Query(CoreQuery, PhoneQuery):
    pass

@strawberry.type
class Mutation():
    pass

schema = strawberry.federation.Schema(
    query=Query,
    enable_federation_2=True,
    extensions=[
        DjangoOptimizerExtension
    ]
)