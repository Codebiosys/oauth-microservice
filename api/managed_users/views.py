from rest_framework import viewsets

from . import serializers
from .mixins import CreateRemoteUserMixin


class ManagedUserViewSet(
    CreateRemoteUserMixin,
    viewsets.GenericViewSet
):
    """ A Viewset that allows a managing user to perform administrative actions
    to managed users.

    create:
    Create a new managed user with default managed user permissions and groups.
    Once the user is created, they're sent a welcome email asking them to reset
    their password.
    """
    serializer_class = serializers.ManagedUserSerializer
