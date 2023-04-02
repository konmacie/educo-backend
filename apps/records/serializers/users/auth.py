from django.contrib.auth import (
    authenticate, get_user_model, update_session_auth_hash)
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

USER_MODEL = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer used in LoginAPIView to validate user credentials.
    Doesn't log user in, just checks credentials and returns User instance
    for valid data. Call Django's login() manually to sign user in.
    ! Call .is_valid() before getting user, to run validators
    Use get_user() to get user instance. Note: before validation and for
    invalid credentials will return None.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    user_permissions = serializers.SerializerMethodField()

    _user = None

    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'password', 'role', 'user_permissions')

    def validate(self, data):
        """
        Validate user credentials and set user instance for valid data.
        """
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user and not user.is_active:
                # Will never proc, since default authentication backend
                # returns None for inactive users.
                # Will work if AllowAllUsersModelBackend used.
                raise serializers.ValidationError('Account deactivated.')
            self._user = user
            # set instance, so user can be serialized by accessing .data
            self.instance = user
        if not self._user:
            raise serializers.ValidationError("Wrong username/password")
        return data

    def get_user(self):
        return self._user

    def get_user_permissions(self, obj):
        return obj.get_all_permissions()
