from django.contrib.auth.forms import (
    UserCreationForm as _UserCreationForm,
    UserChangeForm as _UserChangeForm
)
from django import forms

from .models import User as OneUser


class HiddenAdminFormMixin(object):
    """
    Mixin that hides the superuser in admin forms.
    """
    class Meta:
        model = OneUser
        exclude = ('is_superuser',)
        widgets = {
            'is_superuser': forms.HiddenInput(),
        }


class UserCreationForm(HiddenAdminFormMixin, _UserCreationForm):

    class Meta(_UserCreationForm):
        model = OneUser
        fields = ('email', 'phone')


class UserChangeForm(HiddenAdminFormMixin, _UserChangeForm):

    class Meta:
        model = OneUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_superuser:
            self.fields.pop('is_superuser', None)
