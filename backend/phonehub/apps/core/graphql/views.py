from core.models import PhoneUser
from strawberry.django.views import AsyncGraphQLView
from asgiref.sync import sync_to_async
from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist

class ProtectedGraphQLView(AsyncGraphQLView):
    async def get_context(self, request, response):
        # Allow introspection requests to go through, X-Rover-Introspection is actively denied by gateway.
        if request.headers.get("X-Rover-Introspection") == "1":
            return {
                "request": request,
                "user": None
            }

        user_id = request.headers.get("X-User-ID")

        if not user_id:
            raise GraphQLError(
                message="Unauthorized: User identification not provided.",
                extensions={
                    "code": "UNAUTHENTICATED",
                    "http_status": 401
                }
            )
        
        try:
            user_id = int(user_id)
        except ValueError:
            raise GraphQLError(
                message="Invalid User ID: Must be an integer.",
                extensions={
                    "code": "BAD_INPUT",
                    "http_status": 400
                }
            )
        
        user = None

        try:
            user = await sync_to_async(PhoneUser.objects.get)(external_id=user_id)
        except ObjectDoesNotExist:
            raise GraphQLError(
                message="Unauthorized: User not found",
                extensions={
                    "code": "UNAUTHORIZED",
                    "http_status": 403
                }
            )

        return {
            "request": request,
            "user": user
        }