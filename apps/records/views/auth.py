from django.contrib.auth import login as django_login, logout as django_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.records.serializers.users.auth import LoginSerializer


@method_decorator(sensitive_post_parameters(), "dispatch")
@method_decorator(never_cache, "dispatch")
class LoginAPIView(generics.GenericAPIView):
    """
    Authenticate user with provided credentials,
    start Django session.
    """
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _user = serializer.get_user()

        if _user:
            django_login(self.request, _user)
            return Response(serializer.data)
        return Response(
            {"detail": "Invalid username/password"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        django_logout(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WhoAmIAPIView(generics.RetrieveAPIView):
    """
    Get current authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer

    def get_object(self):
        return self.request.user
