import strawberry
from user.graphql.query import Query as UserQuery
from user.graphql.mutation import Mutation as UserMutation, PublicMutation as PublicUserMutation

from userstatus.graphql.query import Query as UserStatusQuery
from user.graphql.types import PhoneUserType

@strawberry.type
class Query(UserQuery, UserStatusQuery):
    pass

@strawberry.type
class Mutation(UserMutation):
    pass

types = [
    PhoneUserType
]

schema = strawberry.federation.Schema(
    query=Query,
    types=types,
    enable_federation_2=True,
)

@strawberry.type
class PublicQuery:
    pass

@strawberry.type
class PublicMutation(PublicUserMutation):
    pass


public_schema = strawberry.federation.Schema(
    mutation=PublicMutation,
    enable_federation_2=True,
)