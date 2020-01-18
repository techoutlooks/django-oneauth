from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from smartmodels.models import SmartModel

from oneauth.settings import get_setting
from .managers import OneUserManager


class AbstractOneUser(SmartModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_(
        'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    verified = models.BooleanField(default=not get_setting('OTP_ENABLED'), help_text="Is the user verified?")   # OTP
    phone = PhoneNumberField(null=True, blank=True, help_text=_(
        'Optional phone number used for eg. in OTP verification'
    ))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = OneUserManager()

    class Meta:
        db_table = "one_users"
        abstract = True

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        return super(AbstractOneUser, self).delete(using, keep_parents)

    def clean(self):
        super(AbstractOneUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_logged_in(self):
        return type(self).objects.is_user_logged_in(self)


class User(AbstractOneUser):
    class Meta(AbstractOneUser.Meta):
        swappable = 'AUTH_USER_MODEL'
