from core.models import PhoneUser
from strawberry.django.views import AsyncGraphQLView

class PhoneHubGraphQLView(AsyncGraphQLView):
    async def get_context(self, request, response):
        user_id = request.headers.get("X-User-ID")

        user = None
        if user_id:
            user, _ = PhoneUser.objects.get_or_create(external_id=user_id)

        return {
            "request": request,
            "user": user
        }