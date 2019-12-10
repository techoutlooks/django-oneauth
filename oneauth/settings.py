"""
Default Django settings for the `oneauth`.
"""
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from oneauth.apps import AuthConfig

app_label = AuthConfig.name
add_prefix = lambda x: '%s_%s' % (app_label.upper(), x.upper())


DEFAULT_GROUP_PERMS = dict()
DEFAULT_OTP_TOKEN_KEY = 'otp'
DEFAULT_SMS_GATEWAY = 'Fake'

# TODO: useless unless set dynamically on project's settings
# DEFAULT_REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # single sign-on (includes a stateless User object, with permissions, etc.)
#         'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
#     ],
# }
#


def get_setting(name):
    from django.conf import settings

    return {

        # ==== [Permissions]
        # ONEAUTH_PERMISSION_APP: attempt to fix perms from this app only. from `post_migrate` signal.
        # ONEAUTH_GROUP_PERMISSIONS: assigns the permissions that each group should have.
        'PERMISSIONS_APP': getattr(settings, add_prefix('PERMISSIONS_APP'), app_label),
        'GROUP_PERMISSIONS': getattr(settings, add_prefix('GROUP_PERMISSIONS'), DEFAULT_GROUP_PERMS),

        # ==== [OTP token sending]
        # ONEAUTH_OTP_ENABLED: Is OTP on? If not, OTP_* settings are useless.
        # ONEAUTH_OTP_SMS_GATEWAY: Fake, Twilio, Smpp, Whatsapp, etc. Implemented gateways, Cf. `oneauth.gateways`.
        # OTP_EMAIL_SUBJECT: Requires configuring `django.core.mail` correctly.
        'OTP_ENABLED': bool(getattr(settings, add_prefix('OTP_ENABLED'), False)),
        'OTP_TOKEN_KEY': getattr(settings, add_prefix('OTP_TOKEN_KEY'), DEFAULT_OTP_TOKEN_KEY),
        'OTP_SMS_GATEWAY': getattr(settings, add_prefix('SMS_GATEWAY'), DEFAULT_SMS_GATEWAY),
        'OTP_EMAIL_SUBJECT': getattr(settings, add_prefix('OTP_EMAIL_SUBJECT'), _("Your OTP Password")),

    }.get(name)


def check_settings():
    """
    Whether settings.py of project that imports us is properly configured for oneauth.
    """
    try: from rest_framework.settings import api_settings
    except ImportError: pass
    else:
        if not api_settings.DEFAULT_AUTHENTICATION_CLASSES:
            raise ImproperlyConfigured(
                "oneauth requires djangorestframework's `DEFAULT_AUTHENTICATION_CLASSES` to be set. "
                "The value `rest_framework_simplejwt.authentication.JWTAuthentication` is preferred."
            )
