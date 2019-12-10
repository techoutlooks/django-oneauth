from django.contrib.auth import get_user_model
from rest_framework import permissions


class IsAccountValid(permissions.BasePermission):
    """
    Deny requests sent by a user unless his/her account matches few criteria:
    the account must have passed verification checks is_verified
    - deny any requests unless account has not expired

    """
    def has_object_permission(self, request, view, obj):
        """
        Unless POST (account creation, passcode reset), check if:
        the user account is is_verified, has not expired.
        """
        # `has_object_permission is only run if has_permission()=True
        # this ensures that a valid user is always available.
        if not hasattr(request.user, 'account'):
            raise AttributeError(
                '\"account\" property expected on {user_model} instances'.format(
                    user_model=get_user_model())
            )

        if view.action == 'create':
            return True

        account = request.user.account
        return account.is_verified and not account.has_expired
