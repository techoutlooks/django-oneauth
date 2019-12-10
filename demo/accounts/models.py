# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from smartmodels.models import Resource


class Account(Resource):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    bio = models.TextField(_("Biography"))

    def __str__(self):
        padding = 50-len(self.user.email)
        return "Account: {email:\xa0<{padding}} ({phone})".format(
            padding=padding,
            email=self.user.email, phone=self.user.phone
        )

