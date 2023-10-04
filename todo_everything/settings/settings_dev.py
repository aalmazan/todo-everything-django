import os

from .settings_base import *  # noqa: F403, F401

SECRET_KEY = os.getenv(
    "SECRET_KEY", "+xw6)wkb5cy736gu90txxp3dsa_lx%8%hls%x@$e409f-2c7z*"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DATABASE_NAME"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASS"],
        "HOST": os.environ["DATABASE_HOST"],
        "PORT": os.environ["DATABASE_PORT"],
    }
}
