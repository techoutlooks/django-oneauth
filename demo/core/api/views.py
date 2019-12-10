from smartmodels.drf.viewsets import ResourceViewSet

from demo.core.api.serializers import AccountSerializer
from demo.accounts.models import Account


class AccountViewSet(ResourceViewSet):
    """
    ResourceViewSet only allow admin or user-creator by default.

    """
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
