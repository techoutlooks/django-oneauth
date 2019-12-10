import binascii
import hashlib
import hmac
import logging
import struct
import time
from os import urandom

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from oneauth import gateways


logger = logging.getLogger(__name__)


def random_hex(length=20):
    """
    Returns a string of random bytes encoded as hex. This uses
    :func:`os.urandom`, so it should be suitable for generating cryptographic
    keys.
    :param int length: The number of (decoded) bytes to return.
    :returns: A string of hex digits.
    :rtype: bytes
    """
    return binascii.hexlify(urandom(length))


def random_hex_str():
    return random_hex().decode('utf-8')


def hotp(key, counter, digits=6):
    msg = struct.pack(b'>Q', counter)
    hs = hmac.new(key, msg, hashlib.sha1).digest()
    hs = list(iter(hs))

    # Truncate
    offset = hs[19] & 0x0f
    bin_code = (
        (hs[offset] & 0x7f) << 24
        | hs[offset + 1] << 16
        | hs[offset + 2] << 8
        | hs[offset + 3]
    )
    return bin_code % pow(10, digits)


def totp(key, t=None, t0=0, steps=30, digits=6):
    t = int(t or time.time())
    counter = (t - int(t0)) // int(steps)
    return hotp(key, counter, digits)


# If using `sms` method, also set ONEAUTH_OTP_SMS_GATEWAY to one of the available schemes
# eg. `Fake`, `Twilio`, `Smpp`, `Whatsapp`, `Facebook`, etc.
EMAIL = 'email'
SMS = 'sms'
SEND_OTP_METHODS = (
    (EMAIL, _('Email')),
    (SMS, _('SMS')),
)


class TOTPDevice(models.Model):
    """
    https://markusholtermann.eu/2016/09/2-factor-authentication-in-django/
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, default=random_hex_str)
    step = models.PositiveSmallIntegerField(default=30)
    t0 = models.BigIntegerField(default=0)
    last_t = models.BigIntegerField(default=-1)
    method = models.CharField(max_length=10, choices=SEND_OTP_METHODS, null=True, blank=True,
                              help_text=_('Optionally send user the OTP token via `method`'))

    def verify_token(self, other):
        """ Check that the given token is valid by computing the current token and
        checking the current token was generated after the last one and matches the other token. """
        verified = False
        key = binascii.unhexlify(self.key.encode())
        t = time.time()
        token = totp(key, t, self.t0, self.step)

        if t > self.last_t and token == other:
            self.last_t = t
            self.save(update_fields=['last_t'])
            verified = True

        self.user.verified = verified
        self.user.save(update_fields=['verified'])
        return verified

    def send_token(self):
        """ Send the user the OTP token via `self.method`. """
        token = totp(self.key, t=None, t0=self.t0, steps=self.step)
        getattr(gateways, 'send_%s' % self.method)(self, token)
