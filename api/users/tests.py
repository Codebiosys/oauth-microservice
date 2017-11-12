from django.conf import settings
from django.contrib.auth.models import User, Permission, ContentType
from django.test import TestCase

from .apps import UsersConfig
from users.models import PermissionSupport


class UserPermissionsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test_user', 'tester@gmail.com', 'test')

    def test_validate_with_valid_request(self):
        self.client.login(username='test_user', password='test')
        r = self.client.get('/validate/')
        self.assertEqual(r.status_code, 200)

    def test_validate_with_invalid_request(self):
        r = self.client.get('/validate/')
        self.assertEqual(r.status_code, 401)

    def test_permissions_with_valid_request(self):
        self.client.login(username='test_user', password='test')
        r = self.client.get('/permissions/')
        self.assertEqual(r.status_code, 200)

    def test_permissions_with_invalid_request(self):
        r = self.client.get('/permissions/')
        self.assertEqual(r.status_code, 401)


class UsersTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test_user', 'tester@gmail.com', 'test')
        content_type = ContentType.objects.get_for_model(PermissionSupport)
        permission = Permission.objects.create(
            codename='test_permission',
            name='test_permission',
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)

    def test_user_with_valid_request(self):
        self.client.login(username='test_user', password='test')
        r = self.client.get('/user/')
        self.assertEqual(r.status_code, 200)

    def test_user_with_invalid_request(self):
        r = self.client.get('/user/')
        self.assertEqual(r.status_code, 401)

    def test_user_has_permission_with_valid_request(self):
        self.client.login(username='test_user', password='test')
        r = self.client.get('/user/has_permission/?codename=test_permission')
        self.assertEqual(r.status_code, 200)

    def test_user_has_permission_with_invalid_request(self):
        r = self.client.get('/user/has_permission/?codename=test_permission')
        self.assertEqual(r.status_code, 401)


class UsersAppTestCase(TestCase):

    def test_settings_loaded_app(self):
        app_name = UsersConfig.name
        self.assertTrue(app_name in settings.INSTALLED_APPS)
