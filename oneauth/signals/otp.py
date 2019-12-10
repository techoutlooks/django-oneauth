from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from oneauth.models.otp import TOTPDevice


@receiver(post_save, sender=get_user_model())
def create_otp_device(sender, instance, created, **kwargs):
    if created:
        TOTPDevice.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def update_otp_device(sender, instance, **kwargs):
    instance.totpdevice.save()

