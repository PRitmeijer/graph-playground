from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView

from .views import HealthCheckView
from .schema import schema

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('graphql/', csrf_exempt(AsyncGraphQLView.as_view(schema=schema))),
]
