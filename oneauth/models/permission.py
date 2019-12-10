"""
fixes: https://code.djangoproject.com/ticket/11154
source: https://gist.github.com/magopian/7543724
https://stackoverflow.com/questions/15037642/django-proxy-model-permissions-do-not-appear
"""
import sys

from django.apps import apps
from django.contrib.auth.models import Permission as _Permission
from django.core.exceptions import ObjectDoesNotExist

from oneauth.settings import get_setting

# TODO: enable self to set the `permissions_app_name` global var in oneauth.__init__.py
permissions_app_name = None


class Permission(_Permission):
    class Meta:
        proxy = True


def add_perm(perm, group):
    """
    Assigns a permission to a group
    """
    if not isinstance(perm, Permission):
        try:
            app_label, codename = perm.split('.', 1)
        except ValueError:
            raise ValueError("For global permissions, first argument must be in"
                             " format: 'app_label.codename' (is %r)" % perm)
        perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)

    group.permissions.add(perm)
    return perm


def remove_perm(perm, group):
    """
    Removes a permission from a group
    """
    if not isinstance(perm, Permission):
        try:
            app_label, codename = perm.split('.', 1)
        except ValueError:
            raise ValueError("For global permissions, first argument must be in"
                             " format: 'app_label.codename' (is %r)" % perm)
        perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)

    group.permissions.remove(perm)
    return


def check_role_perms(role, perms, current_perms):
    """
    Checks that role (can be user, group or AnonymousUser) has all given permissions,
    granting them if necessary.
    """
    role_permissions = []

    # get all the current permissions, we'll remove these as we verify they should still be granted
    for permission in perms:
        splits = permission.split(".")
        if len(splits) != 2 and len(splits) != 3:
            sys.stderr.write("  invalid msg7 permission %s, ignoring\n" % permission)
            continue

        app = splits[0]
        codenames = []

        if len(splits) == 2:
            codenames.append(splits[1])
        else:
            (object, action) = splits[1:]

            # if this is a wildcard, then query our database for all the permissions that exist on this object
            if action == '*':
                for perm in Permission.objects.filter(codename__endswith="_%s" % object, content_type__app_label=app):
                    codenames.append(perm.codename)
            # otherwise, this is an error, continue
            else:
                sys.stderr.write("  invalid msg7 permission %s, ignoring\n" % permission)
                continue

        if len(codenames) == 0:
            continue

        for codename in codenames:
            # the full codename for this permission
            full_codename = "%s.%s" % (app, codename)

            # this marks all the permissions which should remain
            role_permissions.append(full_codename)

            try:
                add_perm(full_codename, role)
            except ObjectDoesNotExist:
                pass
                # sys.stderr.write("  unknown permission %s, ignoring\n" % permission)

    # remove any that are extra
    for permission in current_perms:
        if isinstance(permission, str):
            key = permission
        else:
            key = "%s.%s" % (permission.content_type.app_label, permission.codename)

        if key not in role_permissions:
            # FIXME: do remove_perm when oneauth is discarded
            # remove_perm(key, role)
            pass
    sys.stdout.write("DEPRECATION WARNING: smartmin & permissions will be removed in release 0.2.0\n")


def add_contenttype_perm(content_type, perm):
    """
    Adds the passed in permission to that content type.  Note that the permission passed
    in should be a single word, or verb.  The proper 'codename' will be generated from that.
    """
    # build our permission slug
    codename = "%s_%s" % (content_type.model, perm)

    # sys.stderr.write("Checking %s permission for %s\n" % (permission, content_type.name))

    # does it already exist
    if not Permission.objects.filter(content_type=content_type, codename=codename):
        Permission.objects.create(content_type=content_type,
                                  codename=codename,
                                  name="Can %s %s" % (perm, content_type.name))
        # sys.stderr.write("Added %s permission for %s\n" % (permission, content_type.name))


def get_perms_app_name():
    """
    Gets the app after which oneauth permissions should be installed.
    This can be specified by `ONEAUTH_PERMISSIONS_APP` in the Django settings or defaults to the last app with models.

    """
    global permissions_app_name

    if not permissions_app_name:
        permissions_app_name = get_setting('PERMISSIONS_APP')

        if not permissions_app_name:
            app_names_with_models = [a.name for a in apps.get_app_configs() if a.models_module is not None]
            if app_names_with_models:
                permissions_app_name = app_names_with_models[-1]

    return permissions_app_name


def is_perms_app(app_config):
    """
    Returns whether this is the app after which permissions should be installed.
    """
    return app_config.name == get_perms_app_name()


__all__ = [
    'Permission',
    'permissions_app_name',
    'add_perm', 'remove_perm', 'check_role_perms', 'add_contenttype_perm', 'get_perms_app_name', 'is_perms_app'
]
