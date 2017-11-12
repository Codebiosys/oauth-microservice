from django.contrib.auth import models
from rest_framework import serializers


class UserPermissionSerializer(serializers.HyperlinkedModelSerializer):
    """ User permissions are serialized/deserialized with the following fields.

    Fields
    ------

    - URL: The URL to the detail view of the Permission. The ID in the URL is
    the codename.

    - name: A human readable name for the Permission. This is what is usually
    shown to the user.

    - codename: The permission's codename. This is set to be the lookup field
    in the URL. This is an internal field in Django's Permissions which can be
    used as a proxy for the the permission's ID.
    """
    class Meta:
        model = models.Permission
        fields = ('url', 'name', 'codename')
        extra_kwargs = {
            'url': {'lookup_field': 'codename'},
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Users are serialized/deserialized with the following fields.

    Fields
    ------

    - username: The given user's username.
    - date_joined: The date the user was created.
    - permissions: The list of permissions that the given user has.
    """
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            'username',
            'date_joined',
            'permissions',
            'first_name',
            'last_name',
            'last_login',
            'email'
        )

    def get_permissions(self, user):
        # Django doesn't have a get_all_permissions method that returns the
        # actual permissions, only the string names, so we have to build our
        # own result queryset to use.
        qs = list(user.user_permissions.all())
        for group in user.groups.all():
            qs += list(group.permissions.all())

        serializer = UserPermissionSerializer(qs, many=True, context=self.context)
        return serializer.data
