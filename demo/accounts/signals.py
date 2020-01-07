from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from smartmodels.helpers import _set_smart_fields, _make_smart_fields, Action

from demo.accounts.models import Account


@receiver(post_save, sender=get_user_model())
def create_user_account(sender, instance, created, **kwargs):
    if created:
        opts = {}
        opts.update(_make_smart_fields(Action.CREATE, instance))
        Account.objects.create(user=instance, **opts)

    _set_smart_fields(instance.account, Action.UPDATE, instance)
    instance.account.save()


# @receiver(post_save, sender=get_user_model())
# def update_user_account(sender, instance, **kwargs):
#     _set_smart_fields(instance.account, Action.UPDATE, instance)
#     instance.account.save()
#

@receiver(post_delete, sender=get_user_model())
def delete_user_account(sender, instance, **kwargs):
    _set_smart_fields(instance.account, Action.DELETE, instance)
    instance.account.delete()


