import os
import datetime
from django.core.exceptions import ImproperlyConfigured

from .common import *

DEBUG = False
TEMPLATE_DEBUG = False


def get_env_variable(var_name):
    """
    Get the environment variable or return exception.

    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "ballotify_beta",
        'USER': get_env_variable("BALLOTIFY_DATABASE_USER"),
        'PASSWORD': get_env_variable("BALLOTIFY_DATABASE_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SECRET_KEY = get_env_variable("BALLOTIFY_SECRET_KEY")

ADMINS = (
    # ('', ''),
)

ALLOWED_HOSTS = ["api.ballotify.com"]

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # TODO: issues with import if use it in correct way
    # 'JWT_PAYLOAD_HANDLER': 'api_v1.core.auth.utils.jwt_payload_handler'
}


SOCIAL_AUTH_FACEBOOK_KEY = get_env_variable("BALLOTIFY_SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = get_env_variable("BALLOTIFY_SOCIAL_AUTH_FACEBOOK_SECRET")


RAVEN_CONFIG = {
    'dsn': get_env_variable("BALLOTIFY_SENTRY_DSN"),
}

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    # ...
    'raven.contrib.django.raven_compat',
)

CORS_ORIGIN_ALLOW_ALL = True
