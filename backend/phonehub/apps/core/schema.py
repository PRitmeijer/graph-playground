import strawberry
from core.graphql.query import Query as CoreQuery
from phone.graphql.query import Query as PhoneQuery

@strawberry.type
class Query(CoreQuery, PhoneQuery):
    pass

@strawberry.type
class Mutation():
    pass

schema = strawberry.federation.Schema(
    query=Query,
    enable_federation_2=True,
)