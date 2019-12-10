from django.contrib.auth.models import Group as _Group


class Group(_Group):
    class Meta:
        proxy = True
    pass
