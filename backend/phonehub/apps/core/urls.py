from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from core.views import HealthCheckView
from core.graphql.schema import schema
from core.graphql.views import PhoneHubGraphQLView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('graphql/', csrf_exempt(PhoneHubGraphQLView.as_view(schema=schema))),
]
