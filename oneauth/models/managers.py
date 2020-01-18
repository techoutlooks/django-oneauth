from django.contrib.auth.base_user import BaseUserManager
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from smartmodels.models import SmartQuerySet
from smartmodels.models.managers import SmartManagerMixin


class SmartUserQuerySet(SmartQuerySet):

    def delete(self, deleted_by=None):
        """
        Fake-delete an entire user queryset.
        ie., only hooked when call looks like: SmartX.objects.filter(**opts).delete()
        """
        return super(SmartUserQuerySet, self).delete(deleted_by=deleted_by, is_active=False)

    def get_current_users(self):
        """
        Queryset of currently logged in users.
        Assumes settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
        https://www.codingforentrepreneurs.com/blog/django-tutorial-get-list-of-current-users
        """
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        # Query all logged in users based on id list
        return self.filter(id__in=user_id_list)


class OneUserManager(SmartManagerMixin, BaseUserManager):
    """
    Custom user model manager using exclusively an `email` as the USERNAME_FIELD,
    that leverages `smartmodels` features, eg. CRUD actions tracking, etc.
    Cf. https://github.com/techoutlooks/django-smartmodels
    """
    queryset_cls = SmartUserQuerySet

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def is_user_logged_in(self, user):
        return user in self.get_queryset().get_current_users()


