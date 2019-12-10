__version__ = '0.1.0dev'
default_app_config = 'oneauth.apps.AuthConfig'

# TODO: Not useful, create behaviour in models.permissions.py that enable to set `permissions_app_name`.
#       Doing so, avoid circular imports.
permissions_app_name = None
