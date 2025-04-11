import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Sentry DSN (replace with your actual DSN from Sentry)
SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,  # Adjust based on your needs
        send_default_pii=True,   # Send personally identifiable information (PII)
    )
