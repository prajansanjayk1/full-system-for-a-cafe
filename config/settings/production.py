from .base import *  # noqa: F403

if SECRET_KEY == "unsafe-dev-key":  # noqa: F405
    raise RuntimeError("DJANGO_SECRET_KEY must be configured in production")
