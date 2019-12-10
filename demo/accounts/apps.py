from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'demo.accounts'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from demo.accounts import signals   # NOQA


