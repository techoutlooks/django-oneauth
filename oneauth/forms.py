from django.contrib.auth.forms import (
    UserCreationForm as _UserCreationForm,
    UserChangeForm as _UserChangeForm
)
from django import forms

from .models import User


class HiddenAdminFormMixin(object):
    """
    Mixin that hides the superuser in admin forms.
    """
    class Meta:
        model = User
        exclude = ('is_superuser',)
        widgets = {
            'is_superuser': forms.HiddenInput(),
        }


class UserCreationForm(HiddenAdminFormMixin, _UserCreationForm):

    class Meta(_UserCreationForm):
        model = User
        fields = ('email', 'phone')


class UserChangeForm(HiddenAdminFormMixin, _UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'phone')
