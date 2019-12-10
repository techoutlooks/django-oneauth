from django.conf import settings
from django.core.mail import send_mail
from django.utils.module_loading import import_string

from oneauth.settings import get_setting


def _get_gateway_class(import_path):
    return import_string(import_path)


def send_sms(device, token):
    gateway = _get_gateway_class(get_setting('SMS_GATEWAY'))()
    gateway.send_sms(device=device, token=token)


def send_email(device, token):
    subject = get_setting('OTP_EMAIL_SUBJECT')
    send_mail(
        subject=subject,
        message="Your OTP password is %s" % token,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[device.user.email]
    )


