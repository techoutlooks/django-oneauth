from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = 'oneauth'
    verbose_name = _('OneAuth')

    def ready(self):
        from oneauth import signals
        from oneauth.settings import check_settings

        # oneauth properly configured?
        check_settings()

        # post_migrate.connect(signals.check_all_permissions)
        post_migrate.connect(signals.check_all_group_permissions)
        post_migrate.connect(signals.fix_proxy_permissions)
