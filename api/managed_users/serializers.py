from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from rest_framework import serializers


UserModel = get_user_model()


managed_user_settings = settings.REMOTE_USER_MANAGEMENT


class ManagedUserSerializer(serializers.ModelSerializer):
    managed_user_default_groups = managed_user_settings['MANAGED_USERS']['DEFAULT_GROUPS']
    managed_user_default_permissions = managed_user_settings['MANAGED_USERS']['DEFAULT_PERMISSIONS']

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')

    def get_default_permissions(self):
        return [
            Permission.objects.get(codename=codename)
            for codename in self.managed_user_default_permissions
        ]

    def get_default_groups(self):
        return [
            Group.objects.get(name=name)
            for name in self.managed_user_default_groups
        ]

    def create(self, validated_data):
        user = UserModel.objects.create(**validated_data)
        user.user_permissions.set(self.get_default_permissions())
        user.groups.set(self.get_default_groups())
        return user
