from django.http import Http404
from rest_framework import viewsets, mixins, filters, response
from rest_framework.decorators import api_view

from . import serializers


class UserPermissionsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """ A simple permissions view that allows a user to check which permissions
    they have. Requests to these endpoints must be authenticated (by default)
    and a user can only see their own permissions.

    list:
    List all of the permissions that a user posesses in a paginated result-set.
    Results contain links to detail views of the given permission. Result-sets
    are paginated with next/previous links and a count of all permissions that
    a user has.

    retrieve:
    Retrieve a given single permission.
    """
    serializer_class = serializers.UserPermissionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('codename',)
    lookup_field = 'codename'

    def get_queryset(self):
        """ Use the current user's permissions only. """
        # Django doesn't have a get_all_permissions method that returns the
        # actual permissions, only the string names, so we have to build our
        # own result queryset to use.
        qs = list(self.request.user.user_permissions.all())
        for group in self.request.user.groups.all():
            qs += list(group.permissions.all())
        return qs

    def get_object(self):
        # Mimic the default QuerySet behavior.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        try:
            return [
                permission for permission in self.get_queryset()
                if permission.codename == self.kwargs[lookup_url_kwarg]
            ][0]
        except IndexError:
            raise Http404()


class UserViewSet(viewsets.GenericViewSet):
    """ Fetch the details of the current logged in user.

    get:
    Retrieve the details for the user that is currently making the request.
    """
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs)
        return response.Response(serializer.data)


@api_view(['GET'])
def validate(request, *args, **kwargs):
    """ By default all API responses are behind authentication, so any
    authenticated request to this endpoint will return a 200 with a valid
    response. Otherwise the permissions and authentication will return
    401 and 403 accordingly.
    """
    return response.Response({
        'message': 'User is valid.'
    })


@api_view(['GET'])
def has_permission(request):
    """ A simple view that expects a `codename` query param and returns whether
    or not the requesting user has such a permission.
    """
    codename = request.GET['codename']
    has_perm = request.user.has_perm(codename)
    return response.Response({
        'message': (
            f'You have the {codename} permission.'
            if has_perm else
            f'You don\'t have the {codename} permission.'
        ),
        'has_permission': has_perm
    })
