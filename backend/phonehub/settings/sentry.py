# settings/sentry.py

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your_sentry_dsn_here",
    integrations=[DjangoIntegration()]
)
