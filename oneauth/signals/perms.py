import sys

from django.apps import apps
from django.conf import settings
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from oneauth.models import is_perms_app, check_role_perms, add_contenttype_perm
from oneauth.settings import get_setting


def fix_proxy_permissions(sender, **kwargs):
    """
    `post_migrate` signal handler that
    copies permissions from the concrete models to the proxy models if any.
    """
    if not is_perms_app(sender):
        return

    perms_counts = dict(perms=[], count=0)
    total_counts = dict(perms=[], concrete_models=[], proxy_models=[])
    stats = dict(total=total_counts, concrete_deleted=perms_counts.copy(), proxy_added=perms_counts.copy())

    for model in apps.get_models():
        opts = model._meta

        if not opts.proxy:
            stats['total']['concrete_models'].append(opts)
            continue

        # The content_type creation is needed for the tests
        proxy_content_type, __ = ContentType.objects.get_or_create(
            app_label=opts.app_label,
            model=opts.model_name,
        )

        concrete_content_type = ContentType.objects.get_for_model(
            model,
            for_concrete_model=True,
        )

        all_model_perms = _get_all_permissions(opts)
        stats['total']['proxy_models'].append(opts.label_lower)
        for codename, name in all_model_perms:

            # Delete the automatically generated permission from Django
            deleted, _rows_count = Permission.objects.filter(
                codename=codename,
                content_type=concrete_content_type,
            ).delete()
            if deleted:
                stats['concrete_deleted']['perms'].append(_rows_count)
                stats['concrete_deleted']['count'] += deleted

            # Create the correct permission for the proxy model
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=proxy_content_type,
                defaults={
                    'name': name,
                })

            if created:
                stats['proxy_added']['perms'].append(perm.codename)
            stats['total']['perms'] = [codename for codename, name in all_model_perms]

    sys.stdout.write('fixed PROXY/CONCRETE/TOTAL=%s/%s/%s new msg7 permissions %s for: %s.\n' % (
        len(stats['proxy_added']['perms']), len(stats['concrete_deleted']['perms']), len(stats['total']['perms']),
        stats['proxy_added']['perms'], stats['total']['proxy_models'],

    ))


def check_all_group_permissions(sender, **kwargs):
    """
    Checks that all the permissions specified in our settings.py are set for our groups.
    """
    if not is_perms_app(sender):
        return

    config = get_setting('GROUP_PERMISSIONS')

    # for each of our items
    for name, permissions in config.items():
        # get or create the group
        (group, created) = Group.objects.get_or_create(name=name)
        if created:
            pass

        check_role_perms(group, permissions, group.permissions.all())


def check_all_permissions(sender, **kwargs):
    """
    This syncdb checks our PERMISSIONS setting in settings.py and makes sure all those permissions
    actually exit.
    """
    if not is_perms_app(sender):
        return

    config = getattr(settings, 'MSG7_PERMISSIONS', dict())

    # for each of our items
    for natural_key, permissions in config.items():
        # if the natural key '*' then that means add to all objects
        if natural_key == '*':
            # for each of our content types
            for content_type in ContentType.objects.all():
                for permission in permissions:
                    add_contenttype_perm(content_type, permission)

        # otherwise, this is on a specific content type, add for each of those
        else:
            app, model = natural_key.split('.')
            try:
                content_type = ContentType.objects.get_by_natural_key(app, model)
            except ContentType.DoesNotExist:
                continue

            # add each permission
            for permission in permissions:
                add_contenttype_perm(content_type, permission)
