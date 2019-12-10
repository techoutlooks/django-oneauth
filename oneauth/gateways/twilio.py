from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import ugettext
from twilio.rest import Client


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Twilio(object):
    """
    Gateway for sending text messages and making phone calls using Twilio_.

    All you need is your Twilio Account SID and Token, as shown in your Twilio
    account dashboard.

    ``TWILIO_ACCOUNT_SID``
      Should be set to your account's SID.

    ``TWILIO_AUTH_TOKEN``
      Should be set to your account's authorization token.

    ``TWILIO_CALLER_ID``
      Should be set to a verified phone number. Twilio_ differentiates between
      numbers verified for making phone calls and sending text messages.

    .. _Twilio: http://www.twilio.com/
    """
    def __init__(self):
        self.client = Client(getattr(settings, 'TWILIO_ACCOUNT_SID'),
                             getattr(settings, 'TWILIO_AUTH_TOKEN'))

    def send_sms(self, device, token):
        body = ugettext('Your authentication token is %s') % token
        self.client.messages.create(
            to=device.number.as_e164,
            from_=getattr(settings, 'TWILIO_CALLER_ID'),
            body=body)
