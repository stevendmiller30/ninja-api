import os

from .base import *  # noqa

# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("PG_HOST"),
        "NAME": os.environ.get("PG_DATABASE"),
        "USER": os.environ.get("PG_USER"),
        "PASSWORD": os.environ.get("PG_PASSWORD"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

STATIC_ROOT = None
STATIC_URL = None
STATICFILES_STORAGE = None

# over-ride env variable for testing purposes
ENV = "unit_test"
