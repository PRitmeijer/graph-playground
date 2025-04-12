from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import HealthCheckView

from strawberry.django.views import AsyncGraphQLView

from .graphql.schema import schema, public_schema


urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('graphql/', csrf_exempt(AsyncGraphQLView.as_view(schema=schema))),
    path('public/graphql/', csrf_exempt(AsyncGraphQLView.as_view(schema=public_schema))),
]
