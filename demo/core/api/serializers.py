from smartmodels.drf.serializers import ResourceSerializer

from demo.accounts.models import Account


class AccountSerializer(ResourceSerializer):
    class Meta:
        model = Account
        fields = '__all__'
