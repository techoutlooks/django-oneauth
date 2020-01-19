from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from smartmodels.drf.serializers.smart import SmartModelSerializer

from oneauth.models import Permission, User, Group
from oneauth.models.otp import SEND_OTP_METHODS
from oneauth.settings import get_setting


class OnePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class OneRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class OneUserSerializer(SmartModelSerializer):
    # in case customer user model might not define a 'username' field,
    # let's strive to keep the api DRY, ie. bound to 'username' anyhow.
    # username = serializers.CharField(source='email', required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    phone = PhoneNumberField(required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    roles = serializers.PrimaryKeyRelatedField(source='groups', many=True, read_only=True)
    permissions = serializers.PrimaryKeyRelatedField(source='user_permissions', many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('user_permissions', 'date_joined', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Create user with credentials and
         attempt to send her random otp token using configured method and/or gateway. """
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        user = super(OneUserSerializer, self).create(validated_data)

        # send otp token thru method if it is recognized
        if get_setting('OTP_ENABLED') and user.method and user.method in list(dict(SEND_OTP_METHODS)):
            user.totpdevice.send_token()

        return user


class OTPValidationError(InvalidToken):
    def __init__(self, user, detail=None, code=None):
        detail = _('OTP verification failed for user {user}. {detail}'.format(user=user, detail=detail))
        super().__init__(detail, code)


class OneTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    One-factor authentication serializer.
    Embeds the user object along with the tokens pair on login.

    If OTP is enabled, and the user have never been validated, OTP token check is performed.
    If the OTP validation succeeds, an access/refresh token pair is returned,
     otherwise, subsequent validation exception is raised.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        otp_field = get_setting('OTP_TOKEN_KEY')
        self.fields[otp_field] = serializers.CharField(required=get_setting('OTP_ENABLED'))

    def verify_otp_token(self, attrs):
        otp_token = attrs.get(get_setting('OTP_TOKEN_KEY'))
        if not otp_token:
            raise OTPValidationError(self.user, 'Missing token.')

        if not self.user.totpdevice.verify_token(otp_token):
            raise OTPValidationError(self.user, 'Wrong token: \'%s\'.' % otp_token)
        return otp_token

    def validate(self, attrs):
        """ 
        If is first-time login, and user-submitted OTP token is incorrect, raise an exception. 
        """

        data = super().validate(attrs)
        if get_setting('OTP_ENABLED') and not self.user.verified:
            otp_token = self.verify_otp_token(attrs)

        # one-factor auth here,
        # let's also include the user's data in the response
        user_data = OneUserSerializer(self.user).data
        data.update(user=user_data)
        return data



