from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from smartmodels.drf.viewsets import SmartViewSet

from oneauth.models import Permission, User, Group as Role
from oneauth.serializers import (
    OneUserSerializer, OnePermissionSerializer, OneRoleSerializer,  # User
    OneTokenObtainPairSerializer  # Auth
)


class OneTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JWT token pair
    to prove the authentication of those credentials.
    If OTP is enabled, request must also supply a valid OTP token, or no JWT token pair will be generated.
    """
    serializer_class = OneTokenObtainPairSerializer


class OneUserViewSet(SmartViewSet):
    serializer_class = OneUserSerializer
    queryset = User.objects.all()


class OnePermissionViewSet(ModelViewSet):
    serializer_class = OnePermissionSerializer
    queryset = Permission.objects.all()


class OneRoleViewSet(ModelViewSet):
    serializer_class = OneRoleSerializer
    queryset = Role.objects.all()
