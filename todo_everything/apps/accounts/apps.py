from django.apps import AppConfig
from django.core.signals import request_finished


class AccountsConfig(AppConfig):
    name = "todo_everything.apps.accounts"

    def ready(self):
        from . import signals

        request_finished.connect(signals.create_profile)
